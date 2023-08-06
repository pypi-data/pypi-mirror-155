import logging
import os
import types
from datetime import datetime, timezone
from typing import Dict, List, Optional, TYPE_CHECKING

import ulid

from ..serialize import decode_body, decode_header_value


logger = logging.getLogger("kolo")


if TYPE_CHECKING:
    # Literal and TypedDict only exist on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import Literal, TypedDict

    class ApiRequest(TypedDict):
        frame_id: str
        method: str
        url: str
        method_and_full_url: str
        body: Optional[str]
        headers: Dict[str, str]
        timestamp: str
        type: Literal["outbound_http_request"]

    class BaseApiResponse(TypedDict):
        frame_id: str
        timestamp: str
        status_code: int
        headers: Dict[str, str]
        type: Literal["outbound_http_response"]
        method: str
        url: str
        method_and_full_url: str

    class ApiResponse(BaseApiResponse, total=False):
        body: str

    class BaseApiInfo(TypedDict):
        request: ApiRequest

    class ApiInfo(BaseApiInfo, total=False):
        response: ApiResponse


def get_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_full_url(frame_locals) -> str:
    scheme = frame_locals["self"].scheme
    host = frame_locals["self"].host
    url = frame_locals["url"]
    return f"{scheme}://{host}{url}"


class ApiRequestFilter:
    use_frames_of_interest = True

    def __init__(self, config) -> None:
        self.config = config
        self.use_frame_boundaries = self.config.get("use_frame_boundaries", False)
        self.data: Dict[str, List[ApiInfo]] = {"api_requests_made": []}
        self.last_response: Optional[ApiResponse] = None

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        # This is equivalent to:
        # self.match_request(frame) or self.match_response(frame) or self.match_urllib(frame)
        # but avoids the function call overhead, which is important for
        # the performance of Kolo's profiling loop.

        filepath = frame.f_code.co_filename
        callable_name = frame.f_code.co_name
        return (
            (
                callable_name == "urlopen"
                and os.path.normpath("urllib3/connectionpool") in filepath
            )
            or (
                callable_name == "request"
                and os.path.normpath("requests/sessions") in filepath
            )
            or (
                callable_name == "do_open"
                and os.path.normpath("urllib/request") in filepath
            )
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        if event == "call" and self.match_request(frame):
            return self.process_api_request_made(frame)
        elif event == "return" and self.match_response(frame):
            return self.process_api_response(frame)
        elif self.match_urllib(frame):
            return self.process_urllib(frame, event)

    def match_request(self, frame: types.FrameType) -> bool:
        filepath = frame.f_code.co_filename
        callable_name = frame.f_code.co_name
        return (
            callable_name == "urlopen"
            and os.path.normpath("urllib3/connectionpool") in filepath
        )

    def match_response(self, frame: types.FrameType) -> bool:
        filepath = frame.f_code.co_filename
        callable_name = frame.f_code.co_name
        return (
            callable_name == "urlopen"
            and os.path.normpath("urllib3/connectionpool") in filepath
        ) or (
            callable_name == "request"
            and os.path.normpath("requests/sessions") in filepath
        )

    def match_urllib(self, frame: types.FrameType) -> bool:
        filepath = frame.f_code.co_filename
        callable_name = frame.f_code.co_name
        return (
            callable_name == "do_open"
            and os.path.normpath("urllib/request") in filepath
        )

    def process_api_request_made(self, frame: types.FrameType):
        frame_locals = frame.f_locals

        request_headers = {
            key: decode_header_value(value)
            for key, value in frame_locals["headers"].items()
        }

        full_url = get_full_url(frame_locals)
        method = frame_locals["method"].upper()
        method_and_full_url = f"{method} {full_url}"

        api_request: ApiRequest = {
            "frame_id": f"frm_{ulid.new()}",
            "method": method,
            "url": full_url,
            "method_and_full_url": method_and_full_url,
            "body": decode_body(frame_locals["body"], request_headers),
            "headers": request_headers,
            "timestamp": get_timestamp(),
            "type": "outbound_http_request",
        }

        if self.use_frame_boundaries:
            return api_request
        else:
            api_info: ApiInfo = {"request": api_request}
            self.data["api_requests_made"].append(api_info)

    def process_api_response(self, frame: types.FrameType):
        if frame.f_code.co_name == "urlopen":
            frame_locals = frame.f_locals

            full_url = get_full_url(frame_locals)
            method = frame_locals["method"].upper()
            method_and_full_url = f"{method} {full_url}"

            response = frame_locals["response"]
            api_response: ApiResponse = {
                "frame_id": f"frm_{ulid.new()}",
                "headers": dict(response.headers),
                "method": method,
                "method_and_full_url": method_and_full_url,
                "status_code": response.status,
                "timestamp": get_timestamp(),
                "type": "outbound_http_response",
                "url": full_url,
            }
            self.last_response = api_response
            if self.use_frame_boundaries:
                return api_response
            else:
                self.data["api_requests_made"][-1]["response"] = api_response
        else:
            response = frame.f_locals["resp"]
            assert self.last_response is not None
            self.last_response["body"] = response.text

    def process_urllib(self, frame: types.FrameType, event: str):
        request = frame.f_locals["req"]
        full_url = request.full_url
        method = request.get_method()
        method_and_full_url = f"{method} {full_url}"
        if event == "call":
            request_headers = {
                key: decode_header_value(value) for key, value in request.header_items()
            }

            api_request: ApiRequest = {
                "frame_id": f"frm_{ulid.new()}",
                "method": method,
                "url": full_url,
                "method_and_full_url": method_and_full_url,
                "body": decode_body(request.data, request_headers),
                "headers": request_headers,
                "timestamp": get_timestamp(),
                "type": "outbound_http_request",
            }

            if self.use_frame_boundaries:
                return api_request
            else:
                api_info: ApiInfo = {"request": api_request}
                self.data["api_requests_made"].append(api_info)

        elif event == "return":  # pragma: no branch
            response = frame.f_locals["r"]
            api_response: ApiResponse = {
                "frame_id": f"frm_{ulid.new()}",
                "method": method,
                "url": full_url,
                "method_and_full_url": method_and_full_url,
                "timestamp": get_timestamp(),
                "status_code": response.status,
                "headers": dict(response.headers),
                "type": "outbound_http_response",
            }
            if self.use_frame_boundaries:
                return api_response
            else:
                self.data["api_requests_made"][-1]["response"] = api_response
