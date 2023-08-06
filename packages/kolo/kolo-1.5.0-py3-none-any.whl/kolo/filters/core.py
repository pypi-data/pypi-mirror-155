import os
import types
from importlib import import_module
from typing import Any, Dict, List, TYPE_CHECKING, Union


if TYPE_CHECKING:
    from typing_extensions import Protocol

    class FrameFilter(Protocol):
        def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
            pass

    ProtoFrameFilter = Union[str, FrameFilter, Dict[str, str]]

    class AdvancedFrameFilter(Protocol):
        config: Dict[str, Any]
        data: Dict[str, Any]
        use_frames_of_interest: bool

        def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
            pass

        def process(
            self,
            frame: types.FrameType,
            event: str,
            arg: object,
            call_frame_ids: List[Dict[str, str]],
        ):
            pass


class HasPath:
    def __init__(self, path: str):
        self.path = path

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        return self.path in frame.f_code.co_filename

    def __repr__(self):
        return f'HasPath("{self.path}")'

    def __eq__(self, other):
        return self.path == other.path


def build_frame_filter(filter: "ProtoFrameFilter") -> "FrameFilter":
    if isinstance(filter, str):
        return HasPath(filter)
    if isinstance(filter, dict):
        filter_path = filter["callable"]
        module_path, _sep, filter_name = filter_path.rpartition(".")
        module = import_module(module_path)
        return getattr(module, filter_name)
    return filter


def exec_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """
    Ignore a frame running a string executed using exec

    We can't show especially interesting information about it, so we skip it.

    A namedtuple is a common example of this case.
    """
    return frame.f_code.co_filename == "<string>"


def frozen_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """
    Ignore all frozen modules

    Frozen modules are compiled into the interpreter, so are almost
    always part of the standard library.

    To opt into showing a frozen module, specify it in include_frames.
    """
    return "<frozen " in frame.f_code.co_filename


def import_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """
    Ignore import machinery

    The import system uses frozen modules, which don't have the same
    "lib/python" string fragment in their filepath as the standard
    library or third party code.
    """
    import_modules = (
        "<builtin>/frozen importlib._bootstrap_external",
        "<builtin>/frozen _structseq",
    )
    return frame.f_code.co_filename in import_modules


def library_filter(frame: types.FrameType, *args, **kwargs) -> bool:
    """
    Ignore library code

    We want to not show library calls, so attempt to filter them out here.
    """
    filepath = frame.f_code.co_filename
    paths = (
        "lib/python",
        "lib/pypy",
        "versions/pypy",
        "/PyPy/",
        "/site-packages/",
        "/x64/lib/",
    )
    if any(os.path.normpath(path) in filepath for path in paths):
        return True
    # Something like \python\python310\lib\ on windows
    return (
        os.path.normpath("/Python/") in filepath
        and os.path.normpath("/lib/") in filepath
    )
