import logging
import os
import sys
import threading
from typing import Any, Callable, Dict, Tuple

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpRequest, HttpResponse

from .config import create_kolo_directory, load_config_from_toml
from .db import load_config_from_db, setup_db
from .profiler import KoloProfiler

logger = logging.getLogger("kolo")

DjangoView = Callable[[HttpRequest], HttpResponse]


class KoloMiddleware:
    def __init__(self, get_response: DjangoView) -> None:
        self.get_response = get_response
        if self.should_enable():
            kolo_directory = create_kolo_directory()
            self.config = load_config_from_toml(kolo_directory / "config.toml")
            self.db_path = setup_db(self.config)
        else:
            message = "Kolo has been disabled via DEBUG setting, KOLO_DISABLE environment variable, or third party profiler"
            raise MiddlewareNotUsed(message)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if self.check_for_third_party_profiler():
            return self.get_response(request)

        self.config = load_config_from_db(self.db_path, self.config)

        filter_config = self.config.get("filters", {})
        ignore_request_paths = filter_config.get("ignore_request_paths", [])
        for path in ignore_request_paths:
            if path in request.path:
                return self.get_response(request)

        self.profiler = KoloProfiler(
            self.db_path,
            include_frames=filter_config.get("include_frames", []),
            ignore_frames=filter_config.get("ignore_frames", []),
            config=self.config,
        )
        self.profiler.initialize_request(request)

        with self.profiler:
            response = self.get_response(request)

        self.profiler.finalize_response(response)

        threading.Thread(
            target=self.profiler.save_request_in_db, name="kolo-save_request_in_db"
        ).start()

        # eventual todo: restore previously set profile
        return response

    def process_view(
        self,
        request: HttpRequest,
        view_func: DjangoView,
        view_args: Tuple[Any],
        view_kwargs: Dict[str, Any],
    ):
        self.profiler.set_url_pattern(request)

    def check_for_third_party_profiler(self) -> bool:
        profiler = sys.getprofile()
        if profiler:
            logger.warning("Profiler %s is active, disabling KoloMiddleware", profiler)
            return True
        return False

    def should_enable(self) -> bool:
        if settings.DEBUG is False:
            logger.debug("DEBUG mode is off, disabling KoloMiddleware")
            return False

        if os.environ.get("KOLO_DISABLE", "false").lower() not in ["false", "0"]:
            logger.debug("KOLO_DISABLE is set, disabling KoloMiddleware")
            return False

        if self.check_for_third_party_profiler():
            return False

        return True
