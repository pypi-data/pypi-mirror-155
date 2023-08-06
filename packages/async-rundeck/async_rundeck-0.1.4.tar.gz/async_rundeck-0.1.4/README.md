[![codecov](https://codecov.io/gh/elda27/async_rundeck/branch/main/graph/badge.svg?token=wo3QBnKsKX)](https://codecov.io/gh/elda27/async_rundeck)

# Asynchronous rundeck API client

This is a rundeck API client implemeneted by aio-http and pydantic.
All API parameters and responses are annotated and user-friendly!

## Installation

```bash
pip install async-rundeck
```

## How to use

```python
import asyncio
from async_rundeck import Rundeck

async def main():
    Rundeck(
        url=rundeck_service, username="admin", password="admin", api_version=41
    )
    project_name = uuid4().hex
    await rundeck.create_project(project_name)

    job_content = (root_dir / "resource" / "Test_job.xml").read_text()
    # Import job
    status = await rundeck.import_jobs(
        project_name,
        job_content,
        content_type="application/xml",
        uuid_option="remove",
    )
    if len(status["succeeded"]) != 1:
      print("Failed to import job")
      return

    jobs = await rundeck.list_jobs(project_name)

    # Execute job
    execution = await rundeck.execute_job(jobs[0].id)
    assert execution is not None

asyncio.run_until_complete(main())
```

## Features

The items checked in the following list are implemented.

- [ ] System Info
- [ ] List Metrics
  - [ ] Metrics Links
  - [ ] Metrics Data
  - [ ] Metrics Healthcheck
  - [ ] Metrics Threading
  - [ ] Metrics Ping
- [ ] User Profile
- [ ] Log Storage
- [ ] Execution Mode
- [ ] Cluster Mode
- [ ] ACLs
- [ ] Jobs
  - [x] List job
  - [x] Run job
  - [x] Import job from file
  - [x] Export job from file
- [ ] Executions
  - [x] Get Executions for a Job
  - [ ] Delete all Executions for a Job
  - [x] Listing Running Executions
  - [ ] Execution Info
  - [x] Upload files for an Execution.
  - [x] List Input Files for an Execution
  - [x] Delete an Execution
  - [ ] Bulk Delete Executions
  - [ ] Execution Query
  - [ ] Execution State
  - [ ] Execution Output
  - [ ] Execution Output with State
  - [ ] Aborting Executions
- [ ] Adhoc
- [ ] Key Storage
  - [ ] Upload keys
  - [ ] List keys
  - [ ] Get Key Metadata
  - [ ] Get Key Contents
  - [ ] Delete Keys
- [ ] Projects
  - [x] Listing Projects
  - [x] Project Creation
  - [x] Getting Project Info
  - [x] Project Deletion
  - [x] Project Configuration
  - [x] Project Configuration Keys
  - [ ] Project Archive Export
  - [ ] Project Archive Export Async
  - [ ] Project Archive Export Status
  - [ ] Project Archive Import
  - [ ] Updating and Listing Resources for a Project
  - [ ] Project Readme File
  - [ ] Project ACLs
- [ ] Listing History
- [ ] Resources/Nodes
- [ ] SCM
