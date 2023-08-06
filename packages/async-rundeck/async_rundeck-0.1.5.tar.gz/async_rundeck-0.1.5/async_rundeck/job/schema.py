from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel, Field

class JobDefinition(BaseModel):
    default_tab: str = Field("nodes", alias="defaultTab", description="The default tab to display when the job is opened")
    description: str = Field("", description="Description of the job")
    execution_enabled: bool = Field(True, alias="executionEnabled", description="Whether the job is enabled for execution")
    id: Optional[str] = Field(None, description="The job's ID")
    loglevel: Literal["DEBUG", "INFO", "WARN", "ERROR"] = Field("INFO", description="The job's log level")
    name: str
    nodeFilterEditable: bool
    plugins: Dict[str, Any] = Field({
        "ExecutionLifecycle": None,
    }, description="plugins")
    schedule_enabled: bool = Field(True, alias="scheduleEnabled", description="Whether the job is enabled for scheduling")
    sequence:
        commands:
        - description: dsd
        exec: dsada
        - args: dsassd dsd
        description: dsd
        fileExtension: sh
        interpreterArgsQuoted: true
        script: |
            @node.os-arch@sd
            dsds

            dsdsd
            dsdsd
        scriptInterpreter: Invacation
        - args: arguments
        description: dsdf
        expandTokenInScriptFile: true
        interpreterArgsQuoted: true
        scriptInterpreter: Invacation
        scriptfile: /erf//c/s/d/xq
        - description: ref
        jobref:
            args: -option1=option -option2=opne
            childNodes: true
            failOnDisable: true
            group: ''
            ignoreNotifications: true
            importOptions: true
            name: FileUpload
            useName: 'true'
            uuid: 08e5cc97-084c-422f-bbf7-ca268c9081d1
        - configuration:
            destinationPath: dest
            echo: 'true'
            pattern: '**/*.txt'
            recursive: 'true'
            sourcePath: source
        description: copy
        nodeStep: true
        type: copyfile
        keepgoing: false
        strategy: node-first
    uuid: 34795772-a3dd-4364-84c5-e686ecc30873
