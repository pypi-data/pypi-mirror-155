import logging
import os
import types
from typing import Any, Dict, List

import ulid

from ..serialize import serialize_function_kwargs


formatter = logging.Formatter()


class LoggingFilter:
    use_frames_of_interest = False

    def __init__(self, config) -> None:
        self.config = config
        self.data: Dict[str, Any] = {}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        co_name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        return (
            event == "return"
            and co_name == "_log"
            and os.path.normpath("/logging/") in filename
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        frame_locals = frame.f_locals
        exc_info = frame_locals["exc_info"]
        traceback = None if exc_info is None else formatter.formatException(exc_info)
        extra = frame_locals["extra"]
        extra = None if extra is None else serialize_function_kwargs(extra)
        return {
            "args": frame_locals["args"],
            "extra": extra,
            "frame_id": f"frm_{ulid.new()}",
            "level": logging.getLevelName(frame_locals["level"]),
            "msg": frame_locals["msg"],
            "stack": formatter.formatStack(frame_locals["sinfo"]),
            "traceback": traceback,
            "type": "log_message",
        }
