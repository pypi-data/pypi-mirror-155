# DON'T CHANGE MANUALLY THIS FILE.
# This file is generated from https://github.com/rundeck/rundeck-api-specs
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from async_rundeck.proto.json_types import (
    Integer,
    Number,
    String,
    Boolean,
    Object,
    File,
)


class User(BaseModel):
    login: Optional[String] = Field(alias="login")
    first_name: Optional[String] = Field(alias="firstName")
    last_name: Optional[String] = Field(alias="lastName")
    email: Optional[String] = Field(alias="email")


class ModifyUserRequest(BaseModel):
    first_name: Optional[String] = Field(alias="firstName")
    last_name: Optional[String] = Field(alias="lastName")
    email: Optional[String] = Field(alias="email")


class Timestamp(BaseModel):
    epoch: Optional[Number] = Field(alias="epoch")
    unit: Optional[String] = Field(alias="unit")
    datetime: Optional[String] = Field(alias="datetime")


class Rundeck(BaseModel):
    version: Optional[String] = Field(alias="version")
    build: Optional[String] = Field(alias="build")
    node: Optional[String] = Field(alias="node")
    base: Optional[String] = Field(alias="base")
    apiversion: Optional[Number] = Field(alias="apiversion")
    server_uuid: Optional[String] = Field(alias="serverUUID")


class Executions(BaseModel):
    active: Optional[Boolean] = Field(alias="active")
    execution_mode: Optional[String] = Field(alias="executionMode")


class Os(BaseModel):
    arch: Optional[String] = Field(alias="arch")
    name: Optional[String] = Field(alias="name")
    version: Optional[String] = Field(alias="version")


class Jvm(BaseModel):
    name: Optional[String] = Field(alias="name")
    vendor: Optional[String] = Field(alias="vendor")
    version: Optional[String] = Field(alias="version")
    implementation_version: Optional[String] = Field(alias="implementationVersion")


class Since(BaseModel):
    epoch: Optional[Number] = Field(alias="epoch")
    unit: Optional[String] = Field(alias="unit")
    datetime: Optional[String] = Field(alias="datetime")


class Uptime(BaseModel):
    duration: Optional[Number] = Field(alias="duration")
    unit: Optional[String] = Field(alias="unit")
    since: Optional[Since] = Field(alias="since")


class LoadAverage(BaseModel):
    unit: Optional[String] = Field(alias="unit")
    average: Optional[Number] = Field(alias="average")


class Cpu(BaseModel):
    load_average: Optional[LoadAverage] = Field(alias="loadAverage")
    processors: Optional[Number] = Field(alias="processors")


class Memory(BaseModel):
    unit: Optional[String] = Field(alias="unit")
    max: Optional[Number] = Field(alias="max")
    free: Optional[Number] = Field(alias="free")
    total: Optional[Number] = Field(alias="total")


class Scheduler(BaseModel):
    running: Optional[Number] = Field(alias="running")
    thread_pool_size: Optional[Number] = Field(alias="threadPoolSize")


class Threads(BaseModel):
    active: Optional[Number] = Field(alias="active")


class Stats(BaseModel):
    uptime: Optional[Uptime] = Field(alias="uptime")
    cpu: Optional[Cpu] = Field(alias="cpu")
    memory: Optional[Memory] = Field(alias="memory")
    scheduler: Optional[Scheduler] = Field(alias="scheduler")
    threads: Optional[Threads] = Field(alias="threads")


class Metrics(BaseModel):
    href: Optional[String] = Field(alias="href")
    content_type: Optional[String] = Field(alias="contentType")


class ThreadDump(BaseModel):
    href: Optional[String] = Field(alias="href")
    content_type: Optional[String] = Field(alias="contentType")


class System(BaseModel):
    timestamp: Optional[Timestamp] = Field(alias="timestamp")
    rundeck: Optional[Rundeck] = Field(alias="rundeck")
    executions: Optional[Executions] = Field(alias="executions")
    os: Optional[Os] = Field(alias="os")
    jvm: Optional[Jvm] = Field(alias="jvm")
    stats: Optional[Stats] = Field(alias="stats")
    metrics: Optional[Metrics] = Field(alias="metrics")
    thread_dump: Optional[ThreadDump] = Field(alias="threadDump")


class SystemInfo(BaseModel):
    system: Optional[System] = Field(alias="system")


class LogStorage(BaseModel):
    enabled: Optional[Boolean] = Field(alias="enabled")
    plugin_name: Optional[String] = Field(alias="pluginName")
    succeeded_count: Optional[Number] = Field(alias="succeededCount")
    failed_count: Optional[Number] = Field(alias="failedCount")
    queued_count: Optional[Number] = Field(alias="queuedCount")
    total_count: Optional[Number] = Field(alias="totalCount")
    incomplete_count: Optional[Number] = Field(alias="incompleteCount")
    missing_count: Optional[Number] = Field(alias="missingCount")


class Storage(BaseModel):
    local_files_present: Optional[Boolean] = Field(alias="localFilesPresent")
    incomplete_filetypes: Optional[List[String]] = Field(alias="incompleteFiletypes")
    queued: Optional[Boolean] = Field(alias="queued")
    failed: Optional[Boolean] = Field(alias="failed")
    date: Optional[String] = Field(alias="date")


class IncompleteLogExecution(BaseModel):
    id: Optional[String] = Field(alias="id")
    project: Optional[String] = Field(alias="project")
    href: Optional[String] = Field(alias="href")
    permalink: Optional[String] = Field(alias="permalink")
    storage: Optional[Storage] = Field(alias="storage")
    errors: Optional[List[String]] = Field(alias="errors")


class IncompleteFileType(Enum):
    Rdlog = "rdlog"
    Statson = "state.json"
    Executioml = "execution.xml"


class IncompleteLogExecutions(BaseModel):
    total: Number = Field(alias="total")
    max: Number = Field(alias="max")
    offset: Number = Field(alias="offset")
    executions: List[IncompleteLogExecution] = Field(alias="executions")


class Server(BaseModel):
    uuid: Optional[String] = Field(alias="uuid")


class Job(BaseModel):
    id: Optional[String] = Field(alias="id")
    name: Optional[String] = Field(alias="name")
    group: Optional[String] = Field(alias="group")
    project: Optional[String] = Field(alias="project")
    description: Optional[String] = Field(alias="description")
    href: Optional[String] = Field(alias="href")
    permalink: Optional[String] = Field(alias="permalink")
    scheduled: Optional[Boolean] = Field(alias="scheduled")
    schedule_enabled: Optional[Boolean] = Field(alias="scheduleEnabled")
    server_node_uuid: Optional[String] = Field(alias="serverNodeUUID")
    server_owner: Optional[String] = Field(alias="serverOwner")
    enabled: Optional[Boolean] = Field(alias="enabled")


class TakeoverScheduleRequest(BaseModel):
    server: Optional[Server] = Field(alias="server")
    project: Optional[String] = Field(alias="project")
    job: Optional[Job] = Field(alias="job")


class JobReference(BaseModel):
    href: Optional[String] = Field(alias="href")
    permalink: Optional[String] = Field(alias="permalink")
    id: Optional[String] = Field(alias="id")
    pervious_owner: Optional[String] = Field(alias="pervious-owner")


class Jobs(BaseModel):
    failed: Optional[List[JobReference]] = Field(alias="failed")
    successfull: Optional[List[JobReference]] = Field(alias="successfull")
    total: Optional[Number] = Field(alias="total")


class TakeoverSchedule(BaseModel):
    project: Optional[String] = Field(alias="project")
    jobs: Optional[Jobs] = Field(alias="jobs")
    server: Optional[Server] = Field(alias="server")


class Self(BaseModel):
    server: Optional[Server] = Field(alias="server")


class TakeoverScheduleResponse(BaseModel):
    takeover_schedule: Optional[TakeoverSchedule] = Field(alias="takeoverSchedule")
    self: Optional[Self] = Field(alias="self")
    message: Optional[String] = Field(alias="message")
    apiversion: Optional[Number] = Field(alias="apiversion")
    success: Optional[Boolean] = Field(alias="success")


class Project(BaseModel):
    description: Optional[String] = Field(alias="description")
    name: Optional[String] = Field(alias="name")
    url: Optional[String] = Field(alias="url")
    config: Optional[Object] = Field(alias="config")


class JobMetadata(BaseModel):
    id: Optional[String] = Field(alias="id")
    name: Optional[String] = Field(alias="name")
    group: Optional[String] = Field(alias="group")
    project: Optional[String] = Field(alias="project")
    description: Optional[String] = Field(alias="description")
    href: Optional[String] = Field(alias="href")
    permalink: Optional[String] = Field(alias="permalink")
    scheduled: Optional[Boolean] = Field(alias="scheduled")
    schedule_enabled: Optional[Boolean] = Field(alias="scheduleEnabled")
    average_duration: Optional[Number] = Field(alias="averageDuration")
    options: Optional[Object] = Field(alias="options")


class JobBulkOperationResponse(BaseModel):
    request_count: Number = Field(alias="requestCount")
    allsuccessful: Boolean = Field(alias="allsuccessful")
    succeeded: Optional[List["BulkJobSucceededInfo"]] = Field(alias="succeeded")
    failed: Optional[List["BulkJobFailedInfo"]] = Field(alias="failed")


class JobInputFileUploadResponse(BaseModel):
    total: Number = Field(alias="total")
    options: Object = Field(alias="options")


class JobInputFileListResponse(BaseModel):
    paging: "Paging" = Field(alias="paging")
    files: List["JobInputFileInfo"] = Field(alias="files")


class FileState(Enum):
    Temp = "temp"
    Deleted = "deleted"
    Expired = "expired"
    Retained = "retained"


class JobInputFileInfo(BaseModel):
    id: String = Field(alias="id")
    user: String = Field(alias="user")
    file_state: FileState = Field(alias="fileState")
    sha: String = Field(alias="sha")
    job_id: String = Field(alias="jobId")
    date_created: String = Field(alias="dateCreated")
    server_node_uuid: String = Field(alias="serverNodeUUID")
    file_name: Optional[String] = Field(alias="fileName")
    size: Optional[Integer] = Field(alias="size")
    expiration_date: String = Field(alias="expirationDate")
    exec_id: Optional[String] = Field(alias="execId")


class BulkJobSucceededInfo(BaseModel):
    id: String = Field(alias="id")
    message: String = Field(alias="message")


class BulkJobFailedInfo(BaseModel):
    id: String = Field(alias="id")
    error_code: String = Field(alias="errorCode")
    message: String = Field(alias="message")


class ExecutionList(BaseModel):
    paging: Optional["Paging"] = Field(alias="paging")
    executions: Optional[List["Execution"]] = Field(alias="executions")


class Status(Enum):
    Running = "running"
    Succeeded = "succeeded"
    Failed = "failed"
    Aborted = "aborted"
    Timedout = "timedout"
    Faileitetry = "failed-with-retry"
    Scheduled = "scheduled"
    Other = "other"


class Dattarted(BaseModel):
    unixtime: Optional[Number] = Field(alias="unixtime")
    date: Optional[String] = Field(alias="date")


class Execution(BaseModel):
    id: Optional[String] = Field(alias="id")
    href: Optional[String] = Field(alias="href")
    permalink: Optional[String] = Field(alias="permalink")
    status: Optional[Status] = Field(alias="status")
    custom_status: Optional[String] = Field(alias="customStatus")
    project: Optional[String] = Field(alias="project")
    user: Optional[String] = Field(alias="user")
    server_uuid: Optional[String] = Field(alias="serverUUID")
    date_started: Optional[Dattarted] = Field(alias="date-started")
    job: Optional[JobMetadata] = Field(alias="job")
    description: Optional[String] = Field(alias="description")
    argstring: Optional[String] = Field(alias="argstring")
    successful_nodes: Optional[List[String]] = Field(alias="successfulNodes")


class JobExecutionDelete(BaseModel):
    failed_count: Optional[Number] = Field(alias="failedCount")
    success_count: Optional[Number] = Field(alias="successCount")
    allsuccessful: Optional[Boolean] = Field(alias="allsuccessful")
    request_count: Optional[Number] = Field(alias="requestCount")
    failures: Optional[List[Object]] = Field(alias="failures")


class AclReference(BaseModel):
    path: Optional[String] = Field(alias="path")
    type: Optional[String] = Field(alias="type")
    name: Optional[String] = Field(alias="name")
    href: Optional[String] = Field(alias="href")


class AclList(BaseModel):
    path: Optional[String] = Field(alias="path")
    type: Optional[String] = Field(alias="type")
    href: Optional[String] = Field(alias="href")
    resources: Optional[List[AclReference]] = Field(alias="resources")


class AclPolicyResponse(BaseModel):
    contents: String = Field(alias="contents")


class InvalidAclPolicyResponse(BaseModel):
    valid: Optional[Boolean] = Field(alias="valid")
    policies: Optional[List[Object]] = Field(alias="policies")


class Loglevel(Enum):
    Debug = "DEBUG"
    Verbose = "VERBOSE"
    Info = "INFO"
    Warn = "WARN"
    Error = "ERROR"


class RetryExecutionRequest(BaseModel):
    arg_string: Optional[String] = Field(alias="argString")
    log_level: Optional[Loglevel] = Field(alias="loglevel")
    as_user: Optional[String] = Field(alias="asUser")
    options: Optional[Object] = Field(alias="options")


class ExecuteJobRequest(BaseModel):
    arg_string: Optional[String] = Field(alias="argString")
    log_level: Optional[Loglevel] = Field(alias="loglevel")
    as_user: Optional[String] = Field(alias="asUser")
    filter: Optional[String] = Field(alias="filter")
    run_at_time: Optional[String] = Field(alias="runAtTime")
    options: Optional[Object] = Field(alias="options")


class StorageKeyMetaType(Enum):
    Private = "private"
    Public = "public"


class Meta(BaseModel):
    rundeck_key_type: Optional[StorageKeyMetaType] = Field(alias="Rundeck-key-type")
    rundeck_content_mask: Optional[String] = Field(alias="Rundeck-content-mask")
    rundeck_content_size: Optional[String] = Field(alias="Rundeck-content-size")
    rundeck_content_type: Optional[String] = Field(alias="Rundeck-content-type")


class StorageKeyMetadata(BaseModel):
    meta: Optional[Meta] = Field(alias="meta")
    url: Optional[String] = Field(alias="url")
    name: Optional[String] = Field(alias="name")
    type: Optional[String] = Field(alias="type")
    path: Optional[String] = Field(alias="path")


class StorageKeyListResponse(BaseModel):
    resources: Optional[List[StorageKeyMetadata]] = Field(alias="resources")
    meta: Optional[Meta] = Field(alias="meta")
    url: Optional[String] = Field(alias="url")
    type: Optional[String] = Field(alias="type")
    path: Optional[String] = Field(alias="path")


class Paging(BaseModel):
    count: Optional[Integer] = Field(alias="count")
    total: Optional[Integer] = Field(alias="total")
    offset: Optional[Integer] = Field(alias="offset")
    max: Optional[Integer] = Field(alias="max")


class ExecutionOutput(BaseModel):
    id: String = Field(alias="id")
    error: Optional[String] = Field(alias="error")
    empty: Optional[Boolean] = Field(alias="empty")
    offset: String = Field(alias="offset")
    completed: Boolean = Field(alias="completed")
    exec_completed: Boolean = Field(alias="execCompleted")
    has_failed_nodes: Boolean = Field(alias="hasFailedNodes")
    exec_state: String = Field(alias="execState")
    last_modified: String = Field(alias="lastModified")
    exec_duration: Number = Field(alias="execDuration")
    percent_loaded: Optional[Number] = Field(alias="percentLoaded")
    total_size: Number = Field(alias="totalSize")
    retry_backoff: Number = Field(alias="retryBackoff")
    cluster_exec: Boolean = Field(alias="clusterExec")
    compacted: Boolean = Field(alias="compacted")
    entries: List["ExecutionOutputEntry"] = Field(alias="entries")


class ExecutionState(BaseModel):
    execution_id: String = Field(alias="executionId")
    server_node: String = Field(alias="serverNode")
    execution_state: Optional["ExecutionStateState"] = Field(alias="executionState")
    completed: Boolean = Field(alias="completed")
    target_nodes: Optional[List[String]] = Field(alias="targetNodes")
    all_nodes: Optional[List[String]] = Field(alias="allNodes")
    step_count: Optional[Number] = Field(alias="stepCount")
    update_time: Optional[String] = Field(alias="updateTime")
    start_time: Optional[String] = Field(alias="startTime")
    end_time: Optional[String] = Field(alias="endTime")
    nodes: Optional[Object] = Field(alias="nodes")
    steps: Optional[List["ExecutionStateStep"]] = Field(alias="steps")


class ExecutionStateState(Enum):
    Succeeded = "SUCCEEDED"
    Failed = "FAILED"
    Running = "RUNNING"
    Waiting = "WAITING"


class ExecutionStateWorkflow(BaseModel):
    completed: Boolean = Field(alias="completed")
    update_time: Optional[String] = Field(alias="updateTime")
    start_time: Optional[String] = Field(alias="startTime")
    end_time: Optional[String] = Field(alias="endTime")
    step_count: Optional[Number] = Field(alias="stepCount")
    target_nodes: Optional[List[String]] = Field(alias="targetNodes")
    all_nodes: Optional[List[String]] = Field(alias="allNodes")
    steps: Optional[List["ExecutionStateStep"]] = Field(alias="steps")


class ExecutionStateNodeState(BaseModel):
    execution_state: ExecutionStateState = Field(alias="executionState")
    stepctx: String = Field(alias="stepctx")


class ExecutionStateStep(BaseModel):
    id: String = Field(alias="id")
    stepctx: String = Field(alias="stepctx")
    node_step: Boolean = Field(alias="nodeStep")
    execution_state: ExecutionStateState = Field(alias="executionState")
    duration: Number = Field(alias="duration")
    start_time: Optional[String] = Field(alias="startTime")
    end_time: Optional[String] = Field(alias="endTime")
    update_time: Optional[String] = Field(alias="updateTime")
    node_states: Optional[Object] = Field(alias="nodeStates")
    has_subworkflow: Optional[Boolean] = Field(alias="hasSubworkflow")
    workflow: Optional[ExecutionStateWorkflow] = Field(alias="workflow")
    parameters: Optional[Object] = Field(alias="parameters")
    parameter_states: Optional[Object] = Field(alias="parameterStates")


class ExecutionStateStepNodeState(BaseModel):
    execution_state: ExecutionStateState = Field(alias="executionState")
    duration: Number = Field(alias="duration")
    start_time: Optional[String] = Field(alias="startTime")
    update_time: Optional[String] = Field(alias="updateTime")
    end_time: Optional[String] = Field(alias="endTime")


class ExecutionOutputEntry(BaseModel):
    time: Optional[String] = Field(alias="time")
    absolute_time: Optional[String] = Field(alias="absolute_time")
    log: Optional[String] = Field(alias="log")
    level: Optional[String] = Field(alias="level")
    stepctx: Optional[String] = Field(alias="stepctx")
    node: Optional[String] = Field(alias="node")


class Jobref(BaseModel):
    name: Optional[String] = Field(alias="name")
    group: Optional[String] = Field(alias="group")
    uuid: Optional[String] = Field(alias="uuid")
    node_step: Optional[String] = Field(alias="nodeStep")
    import_options: Optional[Boolean] = Field(alias="importOptions")


class WorkflowStep(BaseModel):
    jobref: Optional[Jobref] = Field(alias="jobref")
    job_id: Optional[String] = Field(alias="jobId")
    description: Optional[String] = Field(alias="description")
    exec: Optional[String] = Field(alias="exec")
    script: Optional[String] = Field(alias="script")
    scriptfile: Optional[String] = Field(alias="scriptfile")
    scripturl: Optional[String] = Field(alias="scripturl")
    type: Optional[String] = Field(alias="type")
    node_step: Optional[String] = Field(alias="nodeStep")
    workflow: Optional[List["WorkflowStep"]] = Field(alias="workflow")
