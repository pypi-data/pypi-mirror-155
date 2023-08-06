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
from async_rundeck.proto.definitions import Project, Object, File


class ProjectCreateRequest(BaseModel):
    name: Optional[String] = Field(alias="name")
    config: Optional[Object] = Field(alias="config")


class ProjectConfigKeyGetResponse(BaseModel):
    key: Optional[String] = Field(alias="key")
    value: Optional[String] = Field(alias="value")


class ProjectConfigKeySetResponse(BaseModel):
    key: Optional[String] = Field(alias="key")
    value: Optional[String] = Field(alias="value")


class ProjectConfigKeySetRequest(BaseModel):
    value: Optional[String] = Field(alias="value")


class ProjectReadmeGetResponse(BaseModel):
    contents: Optional[String] = Field(alias="contents")


class ReadmeUpdateRequest(BaseModel):
    contents: Optional[String] = Field(alias="contents")


class ProjectMotdGetResponse(BaseModel):
    contents: Optional[String] = Field(alias="contents")


class MotdUpdateRequest(BaseModel):
    contents: Optional[String] = Field(alias="contents")


async def project_list(session: RundeckClient) -> List[Object]:
    """List projects"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url("/api/{version}/projects", version=session.version)
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): List[Object]}[response.status]
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


async def project_create(
    session: RundeckClient, project_create_request: ProjectCreateRequest
) -> Union[Object, None]:
    """Create a new project"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url("/api/{version}/projects", version=session.version)
    async with session.request(
        "POST",
        url,
        data=json.dumps(project_create_request)
        if isinstance(project_create_request, dict)
        else project_create_request.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(201): Object, (409): None}[response.status]
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


async def project_get(session: RundeckClient, project: String) -> Union[Project, None]:
    """Get information about a project"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}", version=session.version, project=project
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): Project, (404): None}[response.status]
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


async def project_delete(session: RundeckClient, project: String) -> None:
    """Delete project"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}", version=session.version, project=project
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


async def project_config_get(
    session: RundeckClient, project: String
) -> Union[Object, None]:
    """Get project config"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/config",
        version=session.version,
        project=project,
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): Object, (404): None}[response.status]
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


async def project_config_update(
    session: RundeckClient, project: String, project_config_update_request: Object
) -> None:
    """Update project config"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/config",
        version=session.version,
        project=project,
    )
    async with session.request(
        "PUT",
        url,
        data=json.dumps(project_config_update_request)
        if isinstance(project_config_update_request, dict)
        else project_config_update_request.json(),
        params=filter_none(dict()),
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


async def project_config_key_get(
    session: RundeckClient, project: String, key: String
) -> ProjectConfigKeyGetResponse:
    """Get project config key"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/config/{key}",
        version=session.version,
        project=project,
        key=key,
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): ProjectConfigKeyGetResponse}[response.status]
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


async def project_config_key_set(
    session: RundeckClient,
    project: String,
    key: String,
    project_config_key_set_request: ProjectConfigKeySetRequest,
) -> ProjectConfigKeySetResponse:
    """Get project config key"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/config/{key}",
        version=session.version,
        project=project,
        key=key,
    )
    async with session.request(
        "PUT",
        url,
        data=json.dumps(project_config_key_set_request)
        if isinstance(project_config_key_set_request, dict)
        else project_config_key_set_request.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): ProjectConfigKeySetResponse}[response.status]
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


async def project_config_key_delete(
    session: RundeckClient, project: String, key: String
) -> None:
    """Delete project config key"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/config/{key}",
        version=session.version,
        project=project,
        key=key,
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


async def project_jobs_export(
    session: RundeckClient,
    project: String,
    *,
    format: Optional[String] = "xml",
    idlist: Optional[String] = None,
    group_path: Optional[String] = None,
    job_filter: Optional[String] = None,
) -> String:
    """Export the job definitions in XML or YAML formats."""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/jobs/export",
        version=session.version,
        project=project,
    )
    async with session.request(
        "GET",
        url,
        data=None,
        params=filter_none(
            dict(
                format=format, idlist=idlist, groupPath=group_path, jobFilter=job_filter
            )
        ),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): String}[response.status]
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


async def project_jobs_import(
    session: RundeckClient,
    project: String,
    file: "File",
    *,
    content_type: Optional[String] = "application/xml",
    accept: Optional[String] = "application/xml",
    file_format: Optional[String] = "xml",
    dupe_option: Optional[String] = "create",
    uuid_option: Optional[String] = "preserve",
) -> "File":
    """Import job definitions in XML or YAML formats."""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/jobs/import",
        version=session.version,
        project=project,
    )
    async with session.request(
        "POST",
        url,
        data=file,
        params=filter_none(
            dict(fileFormat=file_format, dupeOption=dupe_option, uuidOption=uuid_option)
        ),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): File}[response.status]
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


async def project_archive_import(
    session: RundeckClient,
    project: String,
    file: "File",
    *,
    job_uuid_option: Optional[String] = "remove",
    import_executions: Optional[Boolean] = None,
    import_config: Optional[Boolean] = None,
    import_a_c_l: Optional[Boolean] = None,
) -> None:
    """Import project archive."""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/import",
        version=session.version,
        project=project,
    )
    async with session.request(
        "PUT",
        url,
        data=file,
        params=filter_none(
            dict(
                jobUuidOption=job_uuid_option,
                importExecutions=import_executions,
                importConfig=import_config,
                importACL=import_a_c_l,
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


async def project_archive_export_sync(
    session: RundeckClient,
    project: String,
    *,
    execution_ids: Optional[Boolean] = None,
    export_all: Optional[Boolean] = True,
    export_jobs: Optional[Boolean] = None,
    export_executions: Optional[Boolean] = None,
    export_configs: Optional[Boolean] = None,
    export_readmes: Optional[Boolean] = None,
    export_acls: Optional[Boolean] = None,
) -> "File":
    """Export archive of project synchronously"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/export",
        version=session.version,
        project=project,
    )
    async with session.request(
        "GET",
        url,
        data=None,
        params=filter_none(
            dict(
                executionIds=execution_ids,
                exportAll=export_all,
                exportJobs=export_jobs,
                exportExecutions=export_executions,
                exportConfigs=export_configs,
                exportReadmes=export_readmes,
                exportAcls=export_acls,
            )
        ),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): File}[response.status]
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


async def project_readme_get(
    session: RundeckClient, project: String
) -> Union[ProjectReadmeGetResponse, None]:
    """Get the readme.md contents"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/readme.md",
        version=session.version,
        project=project,
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): ProjectReadmeGetResponse, (404): None}[
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


async def project_readme_put(
    session: RundeckClient, project: String, readme_update_request: ReadmeUpdateRequest
) -> None:
    """Create or modify project README.md"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/readme.md",
        version=session.version,
        project=project,
    )
    async with session.request(
        "PUT",
        url,
        data=json.dumps(readme_update_request)
        if isinstance(readme_update_request, dict)
        else readme_update_request.json(),
        params=filter_none(dict()),
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


async def project_readme_delete(session: RundeckClient, project: String) -> None:
    """Delete project README.md"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/readme.md",
        version=session.version,
        project=project,
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


async def project_motd_get(
    session: RundeckClient, project: String
) -> Union[ProjectMotdGetResponse, None]:
    """Get the readme.md contents"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/motd.md",
        version=session.version,
        project=project,
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): ProjectMotdGetResponse, (404): None}[
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


async def project_motd_put(
    session: RundeckClient, project: String, motd_update_request: MotdUpdateRequest
) -> None:
    """Create or modify project MOTD.md"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/motd.md",
        version=session.version,
        project=project,
    )
    async with session.request(
        "PUT",
        url,
        data=json.dumps(motd_update_request)
        if isinstance(motd_update_request, dict)
        else motd_update_request.json(),
        params=filter_none(dict()),
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


async def project_motd_delete(session: RundeckClient, project: String) -> None:
    """Delete project motd.md"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/project/{project}/motd.md",
        version=session.version,
        project=project,
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
