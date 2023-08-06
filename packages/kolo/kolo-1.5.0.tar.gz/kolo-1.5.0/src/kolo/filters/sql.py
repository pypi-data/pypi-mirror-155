import os
import time
import types
from typing import Dict, List, Optional, TYPE_CHECKING

import ulid

from ..serialize import get_callsite_data


if TYPE_CHECKING:
    # Literal and TypedDict only exist on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import Literal, TypedDict
    from ..serialize import UserCodeCallSite

    class QueryInfo(TypedDict, total=False):
        query: str
        query_template: str
        user_code_call_site: Optional[UserCodeCallSite]
        call_timestamp: float
        return_timestamp: float

    class QueryStart(TypedDict):
        frame_id: str
        query_template: str
        user_code_call_site: Optional[UserCodeCallSite]
        call_timestamp: float
        type: Literal["start_sql_query"]

    class QueryEnd(TypedDict, total=False):
        frame_id: str
        query: str
        query_template: str
        user_code_call_site: Optional[UserCodeCallSite]
        return_timestamp: float
        type: Literal["end_sql_query"]


class SQLQueryFilter:
    use_frames_of_interest = False

    def __init__(self, config) -> None:
        self.config = config
        self.use_frame_boundaries = self.config.get("use_frame_boundaries", False)
        self.queries_with_call_site: List[QueryInfo] = []
        self.data = {"queries_with_call_site": self.queries_with_call_site}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        co_name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        return (
            co_name == "_execute"
            and os.path.normpath("/django/db/backends/utils.py") in filename
        ) or co_name == "last_executed_query"

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        co_name = frame.f_code.co_name
        if event == "call" and co_name == "_execute":
            if call_frame_ids:
                user_code_call_site = get_callsite_data(frame, call_frame_ids[-1])
            else:
                user_code_call_site = None

            if self.use_frame_boundaries:
                query_start: QueryStart = {
                    "frame_id": f"frm_{ulid.new()}",
                    "user_code_call_site": user_code_call_site,
                    "call_timestamp": time.time(),
                    "query_template": frame.f_locals["sql"],
                    "type": "start_sql_query",
                }
                return query_start

            query_data: QueryInfo = {
                "user_code_call_site": user_code_call_site,
                "call_timestamp": time.time(),
                "query_template": frame.f_locals["sql"],
            }
            self.queries_with_call_site.append(query_data)

        elif event == "return":
            if self.use_frame_boundaries:
                if co_name == "_execute":
                    if call_frame_ids:
                        user_code_call_site = get_callsite_data(
                            frame, call_frame_ids[-1]
                        )
                    else:
                        user_code_call_site = None

                    query_end: QueryEnd = {
                        "frame_id": f"frm_{ulid.new()}",
                        "user_code_call_site": user_code_call_site,
                        "return_timestamp": time.time(),
                        "query_template": frame.f_locals["sql"],
                        "type": "end_sql_query",
                    }
                    self.last_query = query_end
                    return query_end
                elif co_name == "last_executed_query":  # pragma: no branch
                    from django.db.backends.base.operations import (
                        BaseDatabaseOperations,
                    )

                    if isinstance(  # pragma: no branch
                        frame.f_locals.get("self"), BaseDatabaseOperations
                    ):
                        assert isinstance(arg, str)
                        self.last_query["query"] = arg

            else:
                query_data = self.queries_with_call_site[-1]

                if co_name == "_execute":
                    query_data["return_timestamp"] = time.time()
                elif co_name == "last_executed_query":  # pragma: no branch
                    from django.db.backends.base.operations import (
                        BaseDatabaseOperations,
                    )

                    if isinstance(  # pragma: no branch
                        frame.f_locals.get("self"), BaseDatabaseOperations
                    ):
                        assert isinstance(arg, str)
                        query_data["query"] = arg
