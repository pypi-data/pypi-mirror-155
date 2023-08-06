import inspect
import json
import logging
import sys
import time
import types
from datetime import datetime, timezone
from itertools import chain
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

import toolz
import ulid

from . import __version__
from .db import save_invocation_in_sqlite
from .filters.attrs import attrs_filter
from .filters.celery import CeleryFilter
from .filters.core import (
    build_frame_filter,
    exec_filter,
    frozen_filter,
    import_filter,
    library_filter,
)
from .filters.exception import ExceptionFilter
from .filters.huey import HueyFilter
from .filters.kolo import kolo_filter
from .filters.logging import LoggingFilter
from .filters.requests import ApiRequestFilter
from .filters.sql import SQLQueryFilter
from .filters.unittest import UnitTestFilter
from .git import COMMIT_SHA
from .serialize import (
    frame_path,
    get_callsite_data,
    get_content,
    get_request_body,
    monkeypatch_queryset_repr,
    serialize_locals,
    serialize_potential_json,
)


logger = logging.getLogger("kolo")


if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from .filters.core import AdvancedFrameFilter, FrameFilter
    from .serialize import UserCodeCallSite


def data_merge(values):
    if all(isinstance(value, list) for value in values):
        return list(chain.from_iterable(values))
    return values[0]


class KoloProfiler:
    """
    Collect runtime information about code to view in VSCode.

    include_frames can be passed to enable profiling of standard library
    or third party code.

    ignore_frames can also be passed to disable profiling of a user's
    own code.

    The list should contain fragments of the path to the relevant files.
    For example, to include profiling for the json module the include_frames
    could look like ["/json/"].

    The list may also contain frame filters. A frame filter is a function
    (or other callable) that takes the same arguments as the profilefunc
    passed to sys.setprofile and returns a boolean representing whether
    to allow or block the frame.

    include_frames takes precedence over ignore_frames. A frame that
    matches an entry in each list will be profiled.
    """

    def __init__(
        self, db_path: Path, *, include_frames=(), ignore_frames=(), config=None
    ) -> None:
        self.db_path = db_path
        self.timestamp = datetime.now(timezone.utc)
        self.invocation_id = f"inv_{ulid.new()}"
        self.frames_of_interest: List[Dict[str, Any]] = []
        self.request: Optional[Dict[str, Any]] = None
        self.response: Optional[Dict[str, Any]] = None
        self.config = config if config is not None else {}
        self.include_frames = list(map(build_frame_filter, include_frames))
        self.ignore_frames = list(map(build_frame_filter, ignore_frames))
        self.default_include_frames: List[AdvancedFrameFilter] = [
            CeleryFilter(self.config),
            HueyFilter(self.config),
            ApiRequestFilter(self.config),
            ExceptionFilter(self.config),
            LoggingFilter(self.config),
            SQLQueryFilter(self.config),
            UnitTestFilter(self.config),
        ]
        self.default_ignore_frames: List[FrameFilter] = [
            library_filter,
            frozen_filter,
            import_filter,
            exec_filter,
            attrs_filter,
            kolo_filter,
        ]
        self.call_frame_ids: List[Dict[str, str]] = []
        self.use_frame_boundaries = self.config.get("use_frame_boundaries", False)

    def initialize_request(self, request: "HttpRequest"):
        self.request = {
            "frame_id": f"frm_{ulid.new()}",
            "scheme": request.scheme,
            "method": request.method,
            "path_info": request.path_info,
            "body": get_request_body(request),
            "headers": dict(request.headers),
            "url_pattern": None,
            "type": "django_request",
        }
        if self.use_frame_boundaries:
            self.frames_of_interest.append(self.request)

    def set_url_pattern(self, request: "HttpRequest"):
        assert isinstance(self.request, dict)
        match = request.resolver_match
        # match can be None before url resolving, but we always
        # call set_url_pattern after resolving
        assert match
        self.request["url_pattern"] = {
            "namespace": match.namespace,
            "route": match.route,
            "url_name": match.url_name,
            "view_path": match._func_path,
        }

    def finalize_response(self, response: "HttpResponse") -> None:
        duration = datetime.now(timezone.utc) - self.timestamp

        self.response = {
            "frame_id": f"frm_{ulid.new()}",
            "ms_duration": round(duration.total_seconds() * 1000, 2),
            "status_code": response.status_code,
            "content": get_content(response),
            "headers": dict(response.items()),
            "type": "django_response",
        }
        if self.use_frame_boundaries:
            self.frames_of_interest.append(self.response)

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> None:
        if event in ["c_call", "c_return"]:
            return

        for frame_filter in self.include_frames:
            try:
                if frame_filter(frame, event, arg):
                    self.process_frame(frame, event, arg)
                    return
            except Exception as e:
                logger.debug(
                    "Unexpected exception in include_frames: %s",
                    frame_filter,
                    exc_info=e,
                )
                continue

        for frame_filter in self.ignore_frames:
            try:
                if frame_filter(frame, event, arg):
                    return
            except Exception as e:
                logger.debug(
                    "Unexpected exception in ignore_frames: %s",
                    frame_filter,
                    exc_info=e,
                )
                continue

        for frame_filter in self.default_include_frames:
            try:
                if frame_filter(frame, event, arg):
                    if frame_filter.use_frames_of_interest:
                        self.process_frame(frame, event, arg)
                    with monkeypatch_queryset_repr():
                        frame_data = frame_filter.process(
                            frame, event, arg, self.call_frame_ids
                        )
                    if frame_data:
                        self.frames_of_interest.append(frame_data)
                    return
            except Exception as e:
                logger.debug(
                    "Unexpected exception in default_include_frames: %s",
                    frame_filter,
                    exc_info=e,
                )
                continue

        for frame_filter in self.default_ignore_frames:
            try:
                if frame_filter(frame, event, arg):
                    return
            except Exception as e:
                logger.debug(
                    "Unexpected exception in default_ignore_frames: %s",
                    frame_filter,
                    exc_info=e,
                )
                continue

        try:
            self.process_frame(frame, event, arg)
        except Exception as e:
            logger.debug(
                "Unexpected exception in KoloProfiler.process_frame",
                exc_info=e,
            )

    def __enter__(self):
        sys.setprofile(self)

    def __exit__(self, *exc):
        sys.setprofile(None)

    def save_request_in_db(self) -> None:
        wal_mode = self.config.get("wal_mode", True)
        json_data = {
            "request_id": self.invocation_id,
            "invocation_id": self.invocation_id,
            "current_commit_sha": COMMIT_SHA,
            "timestamp": str(self.timestamp),
            "frames_of_interest": self.frames_of_interest,
            "meta": {
                "version": __version__,
                "use_frame_boundaries": self.use_frame_boundaries,
            },
        }
        if self.use_frame_boundaries:
            save_invocation_in_sqlite(
                self.db_path, self.invocation_id, json.dumps(json_data), wal_mode
            )
            return

        json_data["request"] = self.request
        json_data["response"] = self.response

        filter_data = (filter.data for filter in self.default_include_frames)
        merged_data = toolz.merge_with(data_merge, json_data, *filter_data)

        try:
            dumped_data = json.dumps(merged_data)
        except TypeError:
            merged_data = json_data
            for frame_filter in self.default_include_frames:
                data = frame_filter.data
                try:
                    json.dumps(data)
                except TypeError:
                    name = type(frame_filter).__name__
                    logger.error(
                        f"Unexpected exception when serializing {name} data: {data}"
                    )
                else:
                    merged_data = toolz.merge_with(data_merge, merged_data, data)

            dumped_data = json.dumps(merged_data)

        save_invocation_in_sqlite(
            self.db_path, self.invocation_id, dumped_data, wal_mode
        )

    def process_frame(self, frame: types.FrameType, event: str, arg: object) -> None:
        user_code_call_site: Optional[UserCodeCallSite]
        if event == "call" and self.call_frame_ids:
            user_code_call_site = get_callsite_data(frame, self.call_frame_ids[-1])
        else:
            # If we are a return frame, we don't bother duplicating
            # information for the call frame.
            # If we are the first call frame, we don't have a callsite.
            user_code_call_site = None

        frame_id = f"frm_{ulid.new()}"
        co_name = frame.f_code.co_name
        if event == "call":
            call_frame_data = {
                "frame_id": frame_id,
                "filepath": frame.f_code.co_filename,
                "co_name": co_name,
            }
            self.call_frame_ids.append(call_frame_data)
        elif event == "return":  # pragma: no branch
            self.call_frame_ids.pop()

        with monkeypatch_queryset_repr():
            self.frames_of_interest.append(
                {
                    "id": frame_id,
                    "path": frame_path(frame),
                    "co_name": co_name,
                    "qualname": get_qualname(frame),
                    "event": event,
                    "arg": serialize_potential_json(arg),
                    "locals": serialize_locals(frame.f_locals),
                    "timestamp": time.time(),
                    "type": "frame",
                    "user_code_call_site": user_code_call_site,
                }
            )


def get_qualname(frame: types.FrameType) -> Optional[str]:
    try:
        qualname = frame.f_code.co_qualname  # type: ignore
    except AttributeError:
        pass
    else:
        module = frame.f_globals["__name__"]
        return f"{module}.{qualname}"

    co_name = frame.f_code.co_name
    if co_name == "<module>":  # pragma: no cover
        module = frame.f_globals["__name__"]
        return f"{module}.<module>"

    try:
        outer_frame = frame.f_back
        assert outer_frame
        try:
            function = outer_frame.f_locals[co_name]
        except KeyError:
            try:
                self = frame.f_locals["self"]
            except KeyError:
                cls = frame.f_locals.get("cls")
                if isinstance(cls, type):
                    function = inspect.getattr_static(cls, co_name)
                else:
                    try:
                        qualname = frame.f_locals["__qualname__"]
                    except KeyError:
                        function = frame.f_globals[co_name]
                    else:  # pragma: no cover
                        module = frame.f_globals["__name__"]
                        return f"{module}.{qualname}"
            else:
                function = inspect.getattr_static(self, co_name)
                if isinstance(function, property):
                    function = function.fget

        return f"{function.__module__}.{function.__qualname__}"
    except Exception:
        return None
