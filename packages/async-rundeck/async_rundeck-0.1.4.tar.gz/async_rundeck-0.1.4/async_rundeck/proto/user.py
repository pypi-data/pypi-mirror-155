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
    User,
    ModifyUserRequest,
    ModifyUserRequest,
    ModifyUserRequest,
)


class UserRoleListResponse(BaseModel):
    roles: List[String] = Field(alias="roles")


async def user_list(session: RundeckClient) -> List["User"]:
    """List user profiles"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url("/api/{version}/user/list", version=session.version)
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): List[User]}[response.status]
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


async def user_profile_get(session: RundeckClient) -> User:
    """Get same user profile data"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url("/api/{version}/user/info", version=session.version)
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): User}[response.status]
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


async def user_profile_update(
    session: RundeckClient, user: "ModifyUserRequest"
) -> User:
    """Modify same user profile data"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url("/api/{version}/user/info", version=session.version)
    async with session.request(
        "POST",
        url,
        data=json.dumps(user) if isinstance(user, dict) else user.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): User}[response.status]
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


async def user_profile_get_by_id(session: RundeckClient, user_i_d: String) -> User:
    """Get another user's profile data"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/user/info/{userID}", version=session.version, userID=user_i_d
    )
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): User}[response.status]
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


async def user_profile_update_by_id(
    session: RundeckClient, user_i_d: String, user: ModifyUserRequest
) -> User:
    """Modify another user's profile data"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url(
        "/api/{version}/user/info/{userID}", version=session.version, userID=user_i_d
    )
    async with session.request(
        "POST",
        url,
        data=json.dumps(user) if isinstance(user, dict) else user.json(),
        params=filter_none(dict()),
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): User}[response.status]
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


async def user_role_list(session: RundeckClient) -> UserRoleListResponse:
    """List the roles of the authenticated user"""
    if session.version < 26:
        raise VersionError(
            f"Insufficient api version error, Required >{session.version}"
        )
    url = session.format_url("/api/{version}/user/roles", version=session.version)
    async with session.request(
        "GET", url, data=None, params=filter_none(dict())
    ) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): UserRoleListResponse}[response.status]
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
