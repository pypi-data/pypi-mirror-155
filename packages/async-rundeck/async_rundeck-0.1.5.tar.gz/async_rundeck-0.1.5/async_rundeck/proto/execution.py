# DON'T CHANGE MANUALLY THIS FILE.
# This file is generated from https://github.com/rundeck/rundeck-api-specs
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, parse_obj_as
from async_rundeck.proto.json_types import (
    Integer,
    Number,
    String,
    Boolean,
    Object,
    File,
)
import json
from enum import Enum
from typing import List, Optional, Union
from pydantic import parse_raw_as, BaseModel, Field
from async_rundeck.proto.json_types import (
    Integer,
    Number,
    String,
    Boolean,
    Object,
    File,
)
from async_rundeck.client import RundeckClient
from async_rundeck.misc import filter_none
from async_rundeck.exceptions import RundeckError, VersionError
from async_rundeck.proto.definitions import (
    Execution,
    JobExecutionDelete,
    ExecutionState,
    JobInputFileInfo,
    ExecutionList,
    ExecutionOutput,
)


class ExecutionBulkDeleteRequest(BaseModel):
    ids: List[String] = Field(alias="ids")


class ExecutionInputFilesListResponse(BaseModel):
    files: List["JobInputFileInfo"] = Field(alias="files")


async def execution_status_get(session: RundeckClient, id: String) -> Execution:
    """Get the status of an execution by ID"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/execution/{id}", version=session.version, id=id
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): Execution}[response.status]
                if response_type is None:
                    return None
                elif response_type is String:
                    return obj
                else:
                    return parse_raw_as(response_type, obj)
            except KeyError:
                raise RundeckError(
                    f"Unknwon response code: {session.url}({response.status})"
                )
        else:
            raise RundeckError(
                f"Connection diffused: {session.url}({response.status})\n{obj}"
            )


async def execution_delete(session: RundeckClient, id: String) -> None:
    """Delete an exeuction by ID"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/execution/{id}", version=session.version, id=id
    )
    async with session.request(
        "DELETE", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(204): None}[response.status]
                if response_type is None:
                    return None
                elif response_type is String:
                    return obj
                else:
                    return parse_raw_as(response_type, obj)
            except KeyError:
                raise RundeckError(
                    f"Unknwon response code: {session.url}({response.status})"
                )
        else:
            raise RundeckError(
                f"Connection diffused: {session.url}({response.status})\n{obj}"
            )


async def execution_bulk_delete(
    session: RundeckClient, execution_bulk_delete_request: ExecutionBulkDeleteRequest
) -> JobExecutionDelete:
    """Bulk delete executions"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/executions/delete", version=session.version
    )
    async with session.request(
        "POST",
        url,
        data=json.dumps(execution_bulk_delete_request)
        if isinstance(execution_bulk_delete_request, dict)
        else execution_bulk_delete_request.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobExecutionDelete}[response.status]
                if response_type is None:
                    return None
                elif response_type is String:
                    return obj
                else:
                    return parse_raw_as(response_type, obj)
            except KeyError:
                raise RundeckError(
                    f"Unknwon response code: {session.url}({response.status})"
                )
        else:
            raise RundeckError(
                f"Connection diffused: {session.url}({response.status})\n{obj}"
            )


async def execution_state_get(session: RundeckClient, id: String) -> ExecutionState:
    """Get detail about the node and step state of an execution by ID. The execution can be currently running or completed."""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/execution/{id}/state", version=session.version, id=id
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): ExecutionState}[response.status]
                if response_type is None:
                    return None
                elif response_type is String:
                    return obj
                else:
                    return parse_raw_as(response_type, obj)
            except KeyError:
                raise RundeckError(
                    f"Unknwon response code: {session.url}({response.status})"
                )
        else:
            raise RundeckError(
                f"Connection diffused: {session.url}({response.status})\n{obj}"
            )


async def execution_input_files_list(
    session: RundeckClient, id: String
) -> ExecutionInputFilesListResponse:
    """List input files for an execution"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/execution/{id}/input/files", version=session.version, id=id
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): ExecutionInputFilesListResponse}[
                    response.status
                ]
                if response_type is None:
                    return None
                elif response_type is String:
                    return obj
                else:
                    return parse_raw_as(response_type, obj)
            except KeyError:
                raise RundeckError(
                    f"Unknwon response code: {session.url}({response.status})"
                )
        else:
            raise RundeckError(
                f"Connection diffused: {session.url}({response.status})\n{obj}"
            )


async def execution_list_running(
    session: RundeckClient, project: String
) -> ExecutionList:
    """List job executions"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/executions/running",
        version=session.version,
        project=project,
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): ExecutionList}[response.status]
                if response_type is None:
                    return None
                elif response_type is String:
                    return obj
                else:
                    return parse_raw_as(response_type, obj)
            except KeyError:
                raise RundeckError(
                    f"Unknwon response code: {session.url}({response.status})"
                )
        else:
            raise RundeckError(
                f"Connection diffused: {session.url}({response.status})\n{obj}"
            )


async def execution_query(
    session: RundeckClient,
    project: String,
    *,
    status_filter: Optional[String] = None,
    abortedby_filter: Optional[String] = None,
    user_filter: Optional[String] = None,
    recent_filter: Optional[String] = None,
    older_filter: Optional[String] = None,
    begin: Optional[String] = None,
    adhoc: Optional[Boolean] = None,
) -> None:
    """Query for Executions based on Job or Execution details"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/executions",
        version=session.version,
        project=project,
    )
    async with session.request(
        "GET",
        url,
        data=None,
        params=filter_none(
            dict(
                statusFilter=status_filter,
                abortedbyFilter=abortedby_filter,
                userFilter=user_filter,
                recentFilter=recent_filter,
                olderFilter=older_filter,
                begin=begin,
                adhoc=adhoc,
            )
        ),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): None}[response.status]
                if response_type is None:
                    return None
                elif response_type is String:
                    return obj
                else:
                    return parse_raw_as(response_type, obj)
            except KeyError:
                raise RundeckError(
                    f"Unknwon response code: {session.url}({response.status})"
                )
        else:
            raise RundeckError(
                f"Connection diffused: {session.url}({response.status})\n{obj}"
            )


async def execution_output_get(
    session: RundeckClient,
    id: String,
    *,
    offset: Optional[String] = None,
    maxlines: Optional[Number] = 5000,
) -> ExecutionOutput:
    """List input files for an execution"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/execution/{id}/output", version=session.version, id=id
    )
    async with session.request(
        "GET",
        url,
        data=None,
        params=filter_none(dict(offset=offset, maxlines=maxlines)),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): ExecutionOutput}[response.status]
                if response_type is None:
                    return None
                elif response_type is String:
                    return obj
                else:
                    return parse_raw_as(response_type, obj)
            except KeyError:
                raise RundeckError(
                    f"Unknwon response code: {session.url}({response.status})"
                )
        else:
            raise RundeckError(
                f"Connection diffused: {session.url}({response.status})\n{obj}"
            )
