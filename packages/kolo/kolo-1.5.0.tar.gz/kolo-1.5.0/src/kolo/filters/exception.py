import traceback
import types
from itertools import starmap
from typing import Dict, List, TYPE_CHECKING

import ulid

try:
    from django.db.models import Model as DjangoModel
except ImportError:

    class DjangoModel:  # type: ignore
        """Stub type so isinstance returns False"""


from ..serialize import frame_path, serialize_locals
from .core import library_filter


if TYPE_CHECKING:
    # Literal and TypedDict only exist on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import Literal, TypedDict

    class ExceptionFrameInfo(TypedDict):
        path: str
        co_name: str
        locals: str
        expanded_locals: Dict[str, str]

    class RecordedException(TypedDict):
        # Usually contains one string. Last string in the list is always
        # the one indicating which exception occurred
        exception_summary: List[str]
        exception_with_traceback: List[str]
        exception_frames: List[ExceptionFrameInfo]
        frame_id: str
        bottom_exception_frame: ExceptionFrameInfo
        type: Literal["exception"]


class ExceptionFilter:
    use_frames_of_interest = False

    def __init__(self, config) -> None:
        self.config = config
        self.use_frame_boundaries = self.config.get("use_frame_boundaries", False)
        self.data: Dict[str, RecordedException] = {}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        return (
            event == "call"
            and "django" in frame.f_code.co_filename
            and "handle_uncaught_exception" == frame.f_code.co_name
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        frame_locals = frame.f_locals
        exc_type, exc_value, exc_traceback = frame_locals["exc_info"]

        recorded_exception_frames = []
        expanded_locals_for_frames = []
        for frame_and_line in traceback.walk_tb(exc_traceback):
            frame = frame_and_line[0]

            if not library_filter(frame):
                frame_locals = frame.f_locals

                expanded_locals = {}
                for key, value in frame_locals.items():
                    if hasattr(value, "__dict__") and isinstance(value, DjangoModel):
                        expanded_locals[key] = vars(value)

                recorded_exception_frames.append(frame)
                expanded_locals_for_frames.append(expanded_locals)

        def serialize_exception_frame(frame, expanded_locals) -> "ExceptionFrameInfo":
            return {
                "path": frame_path(frame),
                "co_name": frame.f_code.co_name,
                "locals": serialize_locals(frame.f_locals),
                "expanded_locals": {
                    key: serialize_locals(value)
                    for key, value in expanded_locals.items()
                },
            }

        exception_with_traceback = traceback.format_exception(
            exc_type, exc_value, exc_traceback
        )

        zipped_frames = zip(recorded_exception_frames, expanded_locals_for_frames)
        exception_frames = list(starmap(serialize_exception_frame, zipped_frames))

        exception: RecordedException = {
            "frame_id": f"frm_{ulid.new()}",
            "exception_summary": traceback.format_exception_only(exc_type, exc_value),
            "exception_with_traceback": exception_with_traceback,
            "exception_frames": exception_frames,
            "bottom_exception_frame": exception_frames[-1],
            "type": "exception",
        }
        if self.use_frame_boundaries:
            return exception
        else:
            self.data["exception"] = exception
