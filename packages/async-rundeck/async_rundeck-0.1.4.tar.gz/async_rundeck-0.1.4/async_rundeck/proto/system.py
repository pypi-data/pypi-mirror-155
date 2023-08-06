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
    SystemInfo,
    LogStorage,
    IncompleteLogExecutions,
    TakeoverScheduleResponse,
    Job,
    AclList,
    AclPolicyResponse,
    InvalidAclPolicyResponse,
)


class SystemIncompleteLogStorageExecutionsResumeResponse(BaseModel):
    resumed: Optional[Boolean] = Field(alias="resumed")


class SystemExecutionsEnableResponse(BaseModel):
    execution_mode: Optional[String] = Field(alias="executionMode")


class SystemExecutionsDisableResponse(BaseModel):
    execution_mode: Optional[String] = Field(alias="executionMode")


class SchedulerTakeoverRequest(BaseModel):
    server: Optional[Object] = Field(alias="server")
    project: Optional[String] = Field(alias="project")
    job: Optional[Object] = Field(alias="job")


class SystemAclPolicyCreateRequest(BaseModel):
    contents: String = Field(alias="contents")


class SystemAclPolicyUpdateRequest(BaseModel):
    contents: String = Field(alias="contents")


async def system_info_get(session: RundeckClient) -> SystemInfo:
    """Get Rundeck server information and stats"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url("/api/{version}/system/info", version=session.version)
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): SystemInfo}[response.status]
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


async def system_log_storage_info_get(session: RundeckClient) -> LogStorage:
    """Get Log Storage information and stats"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/system/logstorage", version=session.version
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): LogStorage}[response.status]
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


async def system_incomplete_log_storage_executions_get(
    session: RundeckClient,
) -> IncompleteLogExecutions:
    """List all executions with incomplete log storage"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/system/logstorage/incomplete", version=session.version
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): IncompleteLogExecutions}[response.status]
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


async def system_incomplete_log_storage_executions_resume(
    session: RundeckClient,
) -> SystemIncompleteLogStorageExecutionsResumeResponse:
    """Resume processing incomplete Log Storage uploads"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/system/logstorage/incomplete/resume", version=session.version
    )
    async with session.request(
        "POST", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {
                    (200): SystemIncompleteLogStorageExecutionsResumeResponse
                }[response.status]
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


async def system_executions_enable(
    session: RundeckClient,
) -> SystemExecutionsEnableResponse:
    """Enables executions, allowing adhoc and manual and scheduled jobs to be run"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/system/executions/enable", version=session.version
    )
    async with session.request(
        "POST", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): SystemExecutionsEnableResponse}[response.status]
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


async def system_executions_disable(
    session: RundeckClient,
) -> SystemExecutionsDisableResponse:
    """Disables executions, preventing adhoc and manual and scheduled jobs from running."""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/system/executions/disable", version=session.version
    )
    async with session.request(
        "POST", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): SystemExecutionsDisableResponse}[
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


async def system_scheduler_takeover(
    session: RundeckClient,
    *,
    scheduler_takeover_request: Optional[SchedulerTakeoverRequest] = None,
) -> TakeoverScheduleResponse:
    """Tell a Rundeck server in cluster mode to claim all scheduled jobs from another cluster server"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/scheduler/takeover", version=session.version
    )
    async with session.request(
        "PUT",
        url,
        data=json.dumps(scheduler_takeover_request)
        if isinstance(scheduler_takeover_request, dict)
        else scheduler_takeover_request.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): TakeoverScheduleResponse}[response.status]
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


async def system_scheduled_jobs_for_server(
    session: RundeckClient, uuid: String
) -> List["Job"]:
    """List the scheduled Jobs with their schedule owned by the cluster server with the specified UUID"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/scheduler/server/{uuid}/jobs",
        version=session.version,
        uuid=uuid,
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
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


async def system_scheduled_jobs_list(session: RundeckClient) -> List[Job]:
    """List the scheduled Jobs with their schedule owned by the cluster server"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url("/api/{version}/scheduler/jobs", version=session.version)
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
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


async def system_acl_policy_list(session: RundeckClient) -> Union[AclList, None]:
    """List ACL Policies"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url("/api/{version}/system/acl/", version=session.version)
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): AclList, (404): None}[response.status]
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


async def system_acl_policy_get(
    session: RundeckClient, policy_name: String
) -> Union[AclPolicyResponse, None]:
    """Retrieve the YAML texas of the ACL Policy file"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/system/acl/{policyName}",
        version=session.version,
        policyName=policy_name,
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): AclPolicyResponse, (404): None}[response.status]
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


async def system_acl_policy_create(
    session: RundeckClient,
    policy_name: String,
    *,
    system_acl_policy_create_request: Optional[SystemAclPolicyCreateRequest] = None,
) -> Union[AclPolicyResponse, None, InvalidAclPolicyResponse]:
    """Create a policy"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/system/acl/{policyName}",
        version=session.version,
        policyName=policy_name,
    )
    async with session.request(
        "POST",
        url,
        data=json.dumps(system_acl_policy_create_request)
        if isinstance(system_acl_policy_create_request, dict)
        else system_acl_policy_create_request.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {
                    (201): AclPolicyResponse,
                    (409): None,
                    (400): InvalidAclPolicyResponse,
                }[response.status]
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


async def system_acl_policy_update(
    session: RundeckClient,
    policy_name: String,
    *,
    system_acl_policy_update_request: Optional[SystemAclPolicyUpdateRequest] = None,
) -> Union[AclPolicyResponse, None]:
    """Update policy"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/system/acl/{policyName}",
        version=session.version,
        policyName=policy_name,
    )
    async with session.request(
        "PUT",
        url,
        data=json.dumps(system_acl_policy_update_request)
        if isinstance(system_acl_policy_update_request, dict)
        else system_acl_policy_update_request.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): AclPolicyResponse, (404): None}[response.status]
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


async def system_acl_policy_delete(
    session: RundeckClient, policy_name: String
) -> Union[None, None]:
    """Delete policy"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/system/acl/{policyName}",
        version=session.version,
        policyName=policy_name,
    )
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
