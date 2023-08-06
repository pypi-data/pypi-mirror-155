from ctypes import Union
from typing import Any, Dict, List, Literal, Optional, Tuple
from aiohttp import FormData

from pydantic import parse_raw_as
from async_rundeck.client import RundeckClient

from async_rundeck.proto.definitions import (
    Execution,
    ExecutionList,
    Job,
    JobBulkOperationResponse,
    JobInputFileInfo,
    Project,
)
from async_rundeck import proto
from async_rundeck.exceptions import VersionError, RundeckError
from async_rundeck.proto.job import JobScheduleBulkDisableRequest


class Rundeck:
    def __init__(
        self,
        url: str = None,
        token: str = None,
        username: str = None,
        password: str = None,
        api_version: int = None,
        allow_redirects: bool = None,
    ) -> None:
        self.client = RundeckClient(
            url, token, username, password, api_version, allow_redirects=allow_redirects
        )

    async def __aenter__(self):
        await self.client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self.client.__aexit__(*args)

    async def list_project(self) -> List[Project]:
        """List the existing projects on the server.

        Returns
        -------
        List[Project]
            List of project informations
        """
        return await proto.project_list(self.client)

    async def create_project(
        self, name: str, config: Dict[str, str] = None
    ) -> Optional[Project]:
        """Create a new project

        Parameters
        ----------
        name : str
            name of the project
        config : Dict[str, Any], optional
            configuration of the project, by default None

        Returns
        -------
        Optional[Project]
            Created information about a project
        """
        project = await proto.project_create(
            self.client, proto.ProjectCreateRequest(name=name, config=config)
        )
        if project is None:
            return project
        else:
            return Project.parse_obj(project)

    async def delete_project(self, name: str) -> None:
        """Delete an existing projects on the server. Requires 'delete' authorization.

        Parameters
        ----------
        name : str
            project name
        """
        await proto.project_delete(self.client, project=name)

    async def get_project(self, name: str) -> Optional[Project]:
        """Get a information about a project.

        Parameters
        ----------
        name : str
            name of the project

        Returns
        -------
        Optional[Project]
            Project information
        """
        await proto.project_get(self.client, project=name)

    async def get_project_config(self, name: str) -> Optional[Dict[str, Any]]:
        """Get the configuration of a project.

        Parameters
        ----------
        name : str
            name of the project

        Returns
        -------
        Optional[Dict[str, Any]]
            Project configuration
        """
        return await proto.project_config_get(self.client, project=name)

    async def get_project_config_item(
        self, name: str, key: str
    ) -> Optional[Tuple[str, str]]:
        """Get a configuration item of a project.

        Parameters
        ----------
        name : str
            name of the project
        key : str
            key of the configuration item

        Returns
        -------
        Optional[Tuple[str, str]]
            Project configuration item
        """
        kv = await proto.project_config_key_get(self.client, project=name, key=key)
        return kv.key, kv.value

    async def update_project_config(self, name: str, config: Dict[str, Any]) -> None:
        """Update the configuration of a project.

        Parameters
        ----------
        name : str
            name of the project
        config : Dict[str, Any]
            Project configuration
        """
        await proto.project_config_update(
            self.client, project=name, project_config_update_request=config
        )

    async def update_project_config_item(
        self, name: str, key: str, value: Any
    ) -> Tuple[Optional[str], Optional[str]]:
        """Update a configuration item of a project.

        Parameters
        ----------
        name : str
            name of the project
        key : str
            key of the configuration item
        value : Any
            value of the configuration item

        Returns
        -------
        Tuple[Optional[str], Optional[str]]
            Updated key/value pairs
        """
        response = await proto.project_config_key_set(
            self.client,
            project=name,
            key=key,
            project_config_key_set_request=proto.ProjectConfigKeySetRequest(
                value=value
            ),
        )
        return (response.key, response.value)

    async def delete_project_config_item(self, name: str, key: str) -> None:
        """Delete a configuration item of a project.

        Parameters
        ----------
        name : str
            name of the project
        key : str
            key of the configuration item
        """
        await proto.project_config_key_delete(self.client, project=name, key=key)

    # Jobs functions
    async def get_job_by_name(self, project: str, name: str) -> Optional[Job]:
        """Get a job by name.

        Parameters
        ----------
        name : str
            name of the job

        Returns
        -------
        Optional[Job]
            Job information
        """
        jobs = await self.list_jobs(project)
        for job in jobs:
            if job.name == name:
                return job

    async def list_jobs(
        self,
        project: str,
        *,
        id_list: Optional[str] = None,
        group_path: Optional[str] = "*",
        job_filter: Optional[str] = None,
        job_exact_filter: Optional[str] = None,
        group_path_exact: Optional[str] = None,
        scheduled_filter: Optional[bool] = None,
        server_node_uuid_filter: Optional[str] = None,
        max: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[proto.Job]:
        """List the existing jobs on the server.

        Parameters
        ----------
        project : str
            project name
        id_list : Optional[str], optional
            comma separated list of job ids, by default None
        group_path : Optional[str], optional
            specify a group or partial group path to include all jobs within that group path.
            Set to the special value "-" to match the top level jobs only.
            by default "*", which matches all groups.
        job_filter : Optional[str], optional
             specify a filter for the job Name.
             Matches any job name that contains this value., by default None
        job_exact_filter : Optional[str], optional
            specify an exact job name to match. by default None
        group_path_exact : Optional[str], optional
            group path exact, by default None
        scheduled_filter : Optional[bool], optional
            true/false specify whether to return only scheduled or only not scheduled jobs.
            by default None
        server_node_uuid_filter : Optional[str], optional
            Value: a UUID.
            In cluster mode, use to select scheduled jobs assigned to the server with given UUID.
            by default None
        max: Optional[int]
            limit the maximum amount of results to be received.
            Not implemeneted yet.
        offset: Optional[int]
            use in conjunction with max to paginate the result set.
            Not implemeneted yet.

        Returns
        -------
        List[proto.Job]
            List of job informations
        """
        if max is not None or offset is not None:
            raise NotImplementedError("`max` and `offset` are not implemented yet.")
        return await proto.job_list(
            self.client,
            project=project,
            id_list=id_list,
            group_path=group_path,
            job_filter=job_filter,
            job_exact_filter=job_exact_filter,
            group_path_exact=group_path_exact,
            scheduled_filter=scheduled_filter,
            server_node_uuid_filter=server_node_uuid_filter,
        )

    async def execute_job(
        self,
        job_id: str,
        *,
        arg_string: Optional[str] = None,
        log_level: Optional[proto.Loglevel] = None,
        as_user: Optional[str] = None,
        filter: Optional[str] = None,
        run_at_time: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> proto.Execution:
        """Run a job specified by job_id.

        Parameters:
            job_id: str
                Job id
            argString: str, optional
                argument string to pass to the job, of the form: -opt value -opt2 value ....
            loglevel: LogLevel, optional
                argument specifying the loglevel to use, one of: 'DEBUG','VERBOSE','INFO','WARN','ERROR'
            asUser  str, optional
                specifies a username identifying the user who ran the job. Requires runAs permission.
            Node  str, optional
                filter parameters as described under Using Node Filters
            filter  str, optional
                can be a node filter string.
            runAtTime: str, optional
                 Specify a time to run the job (API v18 or later).
            option. str, optional
                OPTNAME: Option value for option named OPTNAME. If any option.OPTNAME parameters are specified, the argString value is ignored (API v18 or later).
        """
        return await proto.job_execution_run(
            self.client,
            id=job_id,
            request=proto.ExecuteJobRequest(
                arg_string=arg_string,
                log_level=log_level,
                as_user=as_user,
                filter=filter,
                run_at_time=run_at_time,
                options=options,
            ),
        )

    async def delete_job(self, job_id: str) -> None:
        """Delete a job.

        Parameters
        ----------
        job_id : str
            job id
        """
        await proto.job_delete(self.client, id=job_id)

    async def retry_job(
        self, job_id: str, execution_id: int, *, retry_count: int
    ) -> proto.Execution:
        """Retry a job specified by job_id.

        Parameters
        ----------
        job_id : str
            Job id
        execution_id : str
            Execution id
        retry_count : int
            Number of maximum retries
        """
        return await proto.job_retry_execution(
            self.client,
            job_id=job_id,
            execution_id=execution_id,
            request=proto.RetryExecutionRequest(retry_count=retry_count),
        )

    async def export_jobs(
        self,
        project: str,
        *,
        format: Literal["xml", "yaml"] = "xml",
        idlist: Optional[str] = None,
        group_path: Optional[str] = None,
        job_filter: Optional[str] = None,
    ) -> Optional[str]:
        """Export jobs in a project to a file.

        Parameters
        ----------
        project : str
            Project name
        format : "xml"|"yaml", optional
            can be "xml" or "yaml" to specify the output format. Default is "xml"
        The following parameters can also be used to narrow down the result set.

        idlist: str, optional
            specify a comma-separated list of Job IDs to export
        groupPath: str, optional
            specify a group or partial group path to include all jobs within that group path.
        jobFilter: str, optional
            specify a filter for the job Name
        """
        return await proto.project_jobs_export(
            self.client,
            project=project,
            format=format,
            idlist=idlist,
            group_path=group_path,
            job_filter=job_filter,
        )

    async def import_jobs(
        self,
        project: str,
        file: str,
        *,
        content_type: Optional[
            Literal[
                # "x-www-form-urlencoded",
                # "multipart/form-data",
                "application/xml",
                "application/yaml",
            ]
        ] = "x-www-form-urlencoded",
        file_format: Optional[Literal["xml", "yaml"]] = "xml",
        dupe_option: Optional[Literal["skip", "create", "update"]] = "create",
        uuid_option: Optional[Literal["preserve", "remove"]] = "preserve",
    ) -> Optional[Dict[Literal["succeeded", "failed", "skipped"], List[Any]]]:
        """Export jobs in a project to a file.

        Parameters
        ----------
        project : str
            Project name

        content_type: Literal["x-www-form-urlencoded", "multipart/form-data", "application/xml", "application/yaml"], optional
            [Not implemeneted] Content-Type: x-www-form-urlencoded, with a xmlBatch
                request parameter containing the input content
            [Not implemeneted] Content-Type: multipart/form-data multipart MIME request part
                named xmlBatch containing the xml content.
            Content-Type: application/xml, request body is the Jobs XML formatted job definition
            Content-Type: application/yaml, request body is the Jobs YAML formatted job definition

        file_format : Literal["xml", "yaml"], optional
            can be "xml" or "yaml" to specify the input format,
            if multipart of form input is sent. Default is "xml"
        dupe_option:
            A value to indicate the behavior when importing jobs which already exist.
            Value can be "skip", "create", or "update". Default is "create".
        uuid_option:
            Whether to preserve or remove UUIDs from the imported jobs. Allowed values (since V9):
            - preserve: Preserve the UUIDs in imported jobs.
                This may cause the import to fail if the UUID is already used. (Default value).
            - remove: Remove the UUIDs from imported jobs.
                Allows update/create to succeed without conflict on UUID.

        Returns
        -------
        Optional[Dict[Literal["succeeded", "failed", "skipped"], List[Any]]]
            A set of status results.
        """
        if content_type == "multipart/form-data":
            data = FormData()
            data.add_field("xmlBatch", file, content_type=content_type)
        elif content_type == "application/xml":
            data = file
        elif content_type == "application/yaml":
            data = file
        else:
            raise ValueError(f"Unsupported content_type: {content_type}")
        with self.client.context_options(
            {
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": content_type,
                }
            }
        ):
            session = self.client
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
                data=data,
                params=dict(
                    fileFormat=file_format,
                    dupeOption=dupe_option,
                    uuidOption=uuid_option,
                ),
            ) as response:
                obj = await response.text()
                if response.ok:
                    try:
                        response_type = {
                            (200): Dict[
                                Literal["succeeded", "failed", "skipped"], List[Any]
                            ]
                        }[response.status]
                        if response_type is None:
                            return None
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

    async def upload_file_for_job(
        self, job_id: str, option_name: str, file: bytes, file_name: str = None
    ) -> Optional[str]:
        """Upload file for job.

        Parameters
        ----------
        job_id : str
            Job id
        option_name : str
            name of option
        file : bytes
            byte array of the file

        Returns
        -------
        Optional[str]
            id of the uploaded file
        """
        with self.client.context_options(
            {
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/octet-stream",
                }
            }
        ):
            response = await proto.job_input_file_upload(
                self.client, job_id, option_name, file_name=file_name, file=file
            )
            return response.options.get(option_name, None)

    async def list_files_for_job(self, job_id: str) -> List[JobInputFileInfo]:
        """List files for job.

        Parameters
        ----------
        job_id : str

        Returns
        -------
        List[JobInputFileInfo]
            information of uploaded files.
        """
        response = await proto.job_input_file_list(self.client, job_id)
        return response.files

    async def enable_scheduling_job(self, job_id: str) -> bool:
        """Enable scheduling for job.

        Parameters
        ----------
        job_id : str

        Response
        ----------
        bool
            True if succceeded
        """
        response = await proto.job_schedule_enable(self.client, job_id)
        return response.success

    async def disable_scheduling_job(self, job_id: str) -> bool:
        """Disable scheduling for job.

        Parameters
        ----------
        job_id : str

        Response
        ----------
        bool
            True if succceeded
        """
        response = await proto.job_schedule_disable(self.client, job_id)
        return response.success

    async def enable_scheduling_jobs(
        self, job_ids: List[str]
    ) -> JobBulkOperationResponse:
        """Enable scheduling for jobs.

        Parameters
        ----------
        job_ids : st[str]

        Response
        ----------
        JobBulkOperationResponse
            Bulk operation results
        """
        return await proto.job_schedule_bulk_enable(
            self.client, JobScheduleBulkDisableRequest(ids=job_ids)
        )

    async def disable_scheduling_jobs(
        self, job_ids: List[str]
    ) -> JobBulkOperationResponse:
        """Disable scheduling for jobs.

        Parameters
        ----------
        job_ids : List[str]

        Response
        ----------
        JobBulkOperationResponse
            Bulk operation results
        """
        return await proto.job_schedule_bulk_disable(
            self.client, JobScheduleBulkDisableRequest(ids=job_ids)
        )

    # Executions
    async def get_execution(
        self,
        execution_id: str,
        # *,
        # status: Optional[Literal["suceeded", "failed", "aborted", "running"]] = None,
        # max: Optional[int] = None,
        # offset: Optional[int] = None,
    ) -> Execution:
        """Get the list of executions for a job.

        Parameters
        ----------
        execution_id : str
            Execution id
        status: Literal["suceeded", "failed", "aborted", "running"], optional
            the status of executions you want to be returned.
            Must be one of "succeeded", "failed", "aborted", or "running".
            If this parameter is blank or unset, include all executions.
        max: int, optional
            indicate the maximum number of results to return.
            If unspecified, all results will be returned.
        offset: int, optional
            indicate the 0-indexed offset for the first result to return.

        Returns
        -------
        List[proto.Execution]
            List of executions
        """
        return await proto.execution_status_get(self.client, id=execution_id)

    async def delete_execution(self, execution_id: str) -> None:
        """Delete an execution.

        Parameters
        ----------
        execution_id : str
            Execution id
        """
        return await proto.execution_delete(self.client, execution_id)

    async def list_running_executions(self, project: str) -> ExecutionList:
        """List running executions.

        Parameters
        ----------
        project : str
            Project name

        Returns
        -------
        ExecutionList
            executions
        """
        return await proto.execution_list_running(self.client, project=project)
