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
    Job,
    ExecutionList,
    Execution,
    ExecuteJobRequest,
    ExecuteJobRequest,
    JobExecutionDelete,
    RetryExecutionRequest,
    RetryExecutionRequest,
    JobMetadata,
    JobBulkOperationResponse,
    JobInputFileUploadResponse,
    File,
    JobInputFileListResponse,
    JobInputFileInfo,
    WorkflowStep,
)


class JobBulkDeleteRequest(BaseModel):
    ids: List[String] = Field(alias="ids")


class JobExecutionEnableResponse(BaseModel):
    success: Optional[Boolean] = Field(alias="success")


class JobExecutionDisableResponse(BaseModel):
    success: Optional[Boolean] = Field(alias="success")


class JobScheduleEnableResponse(BaseModel):
    success: Optional[Boolean] = Field(alias="success")


class JobScheduleDisableResponse(BaseModel):
    success: Optional[Boolean] = Field(alias="success")


class JobExecutionBulkEnableRequest(BaseModel):
    ids: List[String] = Field(alias="ids")


class JobExecutionBulkDisableRequest(BaseModel):
    ids: List[String] = Field(alias="ids")


class JobScheduleBulkEnableRequest(BaseModel):
    ids: List[String] = Field(alias="ids")


class JobScheduleBulkDisableRequest(BaseModel):
    ids: List[String] = Field(alias="ids")


class JobWorkflowGetResponse(BaseModel):
    workflow: List["WorkflowStep"] = Field(alias="workflow")


async def job_list(
    session: RundeckClient,
    project: String,
    *,
    id_list: Optional[String] = None,
    group_path: Optional[String] = "*",
    job_filter: Optional[String] = None,
    job_exact_filter: Optional[String] = None,
    group_path_exact: Optional[String] = None,
    scheduled_filter: Optional[Boolean] = None,
    server_node_uuid_filter: Optional[String] = None,
) -> List["Job"]:
    """List the jobs that exist for a project"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/jobs",
        version=session.version,
        project=project,
    )
    async with session.request(
        "GET",
        url,
        data=None,
        params=filter_none(
            dict(
                idList=id_list,
                groupPath=group_path,
                jobFilter=job_filter,
                jobExactFilter=job_exact_filter,
                groupPathExact=group_path_exact,
                scheduledFilter=scheduled_filter,
                serverNodeUUIDFilter=server_node_uuid_filter,
            )
        ),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): List[Job]}[response.status]
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


async def job_execution_list(session: RundeckClient, id: String) -> ExecutionList:
    """List job executions"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/job/{id}/executions", version=session.version, id=id
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


async def job_execution_run(
    session: RundeckClient, id: String, *, request: Optional["ExecuteJobRequest"] = None
) -> Execution:
    """Run the specified job"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/job/{id}/executions", version=session.version, id=id
    )
    async with session.request(
        "POST",
        url,
        data=json.dumps(request) if isinstance(request, dict) else request.json(),
        params=filter_none(dict()),
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


async def job_execution_delete(
    session: RundeckClient, id: Integer
) -> JobExecutionDelete:
    """Delete all job executions"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/job/{id}/executions", version=session.version, id=id
    )
    async with session.request(
        "DELETE", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(204): JobExecutionDelete}[response.status]
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


async def job_retry_execution(
    session: RundeckClient,
    job_id: String,
    execution_id: Integer,
    *,
    request: Optional["RetryExecutionRequest"] = None,
) -> ExecutionList:
    """Retry a failed job execution on failed nodes only or on the same as the execution. This is the same functionality as the `Retry Failed Nodes ...` button on the execution page."""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/job/{jobID}/retry/{executionID}",
        version=session.version,
        jobID=job_id,
        executionID=execution_id,
    )
    async with session.request(
        "POST",
        url,
        data=json.dumps(request) if isinstance(request, dict) else request.json(),
        params=filter_none(dict()),
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


async def job_get(
    session: RundeckClient, id: String, *, format: Optional[String] = "xml"
) -> Union["File", None]:
    """Export a single job definition in XML or YAML formats."""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url("/api/{version}/job/{id}", version=session.version, id=id)
    async with session.request(
        "GET", url, data=None, params=filter_none(dict(format=format))
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): File, (404): None}[response.status]
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


async def job_delete(session: RundeckClient, id: String) -> Union[None, None]:
    """Delete a single job definition."""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url("/api/{version}/job/{id}", version=session.version, id=id)
    async with session.request(
        "DELETE", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(204): None, (404): None}[response.status]
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


async def job_info_get(session: RundeckClient, id: String) -> JobMetadata:
    """Get metadata about a specific job."""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/job/{id}/info", version=session.version, id=id
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobMetadata}[response.status]
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


async def job_bulk_delete(
    session: RundeckClient, job_bulk_delete_request: JobBulkDeleteRequest
) -> JobBulkOperationResponse:
    """Delete multiple job definitions at once"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url("/api/{version}/jobs/delete", version=session.version)
    async with session.request(
        "POST",
        url,
        data=json.dumps(job_bulk_delete_request)
        if isinstance(job_bulk_delete_request, dict)
        else job_bulk_delete_request.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobBulkOperationResponse}[response.status]
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


async def job_execution_enable(
    session: RundeckClient, id: String
) -> JobExecutionEnableResponse:
    """Enable executions for a job. (ACL requires toggle_execution action for a job.)"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/job/{id}/execution/enable", version=session.version, id=id
    )
    async with session.request(
        "POST", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobExecutionEnableResponse}[response.status]
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


async def job_execution_disable(
    session: RundeckClient, id: String
) -> JobExecutionDisableResponse:
    """Disable all executions for a job (scheduled or manual). (ACL requires toggle_execution action for a job.)"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/job/{id}/execution/disable", version=session.version, id=id
    )
    async with session.request(
        "POST", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobExecutionDisableResponse}[response.status]
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


async def job_schedule_enable(
    session: RundeckClient, id: String
) -> JobScheduleEnableResponse:
    """Enable the schedule for a job. (ACL requires toggle_schedule action for a job.)"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/job/{id}/schedule/enable", version=session.version, id=id
    )
    async with session.request(
        "POST", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobScheduleEnableResponse}[response.status]
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


async def job_schedule_disable(
    session: RundeckClient, id: String
) -> JobScheduleDisableResponse:
    """Disable the schedule for a job. (ACL requires toggle_schedule action for a job.)"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/job/{id}/schedule/disable", version=session.version, id=id
    )
    async with session.request(
        "POST", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobScheduleDisableResponse}[response.status]
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


async def job_execution_bulk_enable(
    session: RundeckClient,
    job_execution_bulk_enable_request: JobExecutionBulkEnableRequest,
) -> JobBulkOperationResponse:
    """Bulk enable job executions"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/jobs/execution/enable", version=session.version
    )
    async with session.request(
        "POST",
        url,
        data=json.dumps(job_execution_bulk_enable_request)
        if isinstance(job_execution_bulk_enable_request, dict)
        else job_execution_bulk_enable_request.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobBulkOperationResponse}[response.status]
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


async def job_execution_bulk_disable(
    session: RundeckClient,
    job_execution_bulk_disable_request: JobExecutionBulkDisableRequest,
) -> JobBulkOperationResponse:
    """Bulk disable job executions"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/jobs/execution/disable", version=session.version
    )
    async with session.request(
        "POST",
        url,
        data=json.dumps(job_execution_bulk_disable_request)
        if isinstance(job_execution_bulk_disable_request, dict)
        else job_execution_bulk_disable_request.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobBulkOperationResponse}[response.status]
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


async def job_schedule_bulk_enable(
    session: RundeckClient,
    job_schedule_bulk_enable_request: JobScheduleBulkEnableRequest,
) -> JobBulkOperationResponse:
    """Bulk enable job schedule"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/jobs/schedule/enable", version=session.version
    )
    async with session.request(
        "POST",
        url,
        data=json.dumps(job_schedule_bulk_enable_request)
        if isinstance(job_schedule_bulk_enable_request, dict)
        else job_schedule_bulk_enable_request.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobBulkOperationResponse}[response.status]
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


async def job_schedule_bulk_disable(
    session: RundeckClient,
    job_schedule_bulk_disable_request: JobScheduleBulkDisableRequest,
) -> JobBulkOperationResponse:
    """Bulk disable job schedule"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/jobs/schedule/disable", version=session.version
    )
    async with session.request(
        "POST",
        url,
        data=json.dumps(job_schedule_bulk_disable_request)
        if isinstance(job_schedule_bulk_disable_request, dict)
        else job_schedule_bulk_disable_request.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobBulkOperationResponse}[response.status]
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


async def job_input_file_upload(
    session: RundeckClient,
    id: String,
    option_name: String,
    file_name: String,
    file: "File",
) -> JobInputFileUploadResponse:
    """Upload file as job option"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/job/{id}/input/file", version=session.version, id=id
    )
    async with session.request(
        "POST",
        url,
        data=file,
        params=filter_none(dict(optionName=option_name, fileName=file_name)),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobInputFileUploadResponse}[response.status]
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


async def job_input_file_list(
    session: RundeckClient, id: String
) -> JobInputFileListResponse:
    """List uploaded input files for job"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/job/{id}/input/files", version=session.version, id=id
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobInputFileListResponse}[response.status]
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


async def job_input_file_info_get(
    session: RundeckClient, id: String
) -> JobInputFileInfo:
    """Get job input file info"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/jobs/file/{id}", version=session.version, id=id
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobInputFileInfo}[response.status]
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


async def job_workflow_get(
    session: RundeckClient, id: String
) -> JobWorkflowGetResponse:
    """Get job workflow tree."""
    if session.version < 34:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/job/{id}/workflow", version=session.version, id=id
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): JobWorkflowGetResponse}[response.status]
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
