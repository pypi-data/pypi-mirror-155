# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_rundeck', 'async_rundeck.job', 'async_rundeck.proto']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pytest-asyncio>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'async-rundeck',
    'version': '0.1.5',
    'description': 'Asynchronous rundeck API client',
    'long_description': '[![codecov](https://codecov.io/gh/elda27/async_rundeck/branch/main/graph/badge.svg?token=wo3QBnKsKX)](https://codecov.io/gh/elda27/async_rundeck)\n\n# Asynchronous rundeck API client\n\nThis is a rundeck API client implemeneted by aio-http and pydantic.\nAll API parameters and responses are annotated and user-friendly!\n\n## Installation\n\n```bash\npip install async-rundeck\n```\n\n## How to use\n\n```python\nimport asyncio\nfrom async_rundeck import Rundeck\n\nasync def main():\n    Rundeck(\n        url=rundeck_service, username="admin", password="admin", api_version=41\n    )\n    project_name = uuid4().hex\n    await rundeck.create_project(project_name)\n\n    job_content = (root_dir / "resource" / "Test_job.xml").read_text()\n    # Import job\n    status = await rundeck.import_jobs(\n        project_name,\n        job_content,\n        content_type="application/xml",\n        uuid_option="remove",\n    )\n    if len(status["succeeded"]) != 1:\n      print("Failed to import job")\n      return\n\n    jobs = await rundeck.list_jobs(project_name)\n\n    # Execute job\n    execution = await rundeck.execute_job(jobs[0].id)\n    assert execution is not None\n\nasyncio.run_until_complete(main())\n```\n\n## Features\n\nThe items checked in the following list are implemented.\n\n- [ ] System Info\n- [ ] List Metrics\n  - [ ] Metrics Links\n  - [ ] Metrics Data\n  - [ ] Metrics Healthcheck\n  - [ ] Metrics Threading\n  - [ ] Metrics Ping\n- [ ] User Profile\n- [ ] Log Storage\n- [ ] Execution Mode\n- [ ] Cluster Mode\n- [ ] ACLs\n- [ ] Jobs\n  - [x] List job\n  - [x] Run job\n  - [x] Import job from file\n  - [x] Export job from file\n- [ ] Executions\n  - [x] Get Executions for a Job\n  - [ ] Delete all Executions for a Job\n  - [x] Listing Running Executions\n  - [ ] Execution Info\n  - [x] Upload files for an Execution.\n  - [x] List Input Files for an Execution\n  - [x] Delete an Execution\n  - [ ] Bulk Delete Executions\n  - [ ] Execution Query\n  - [ ] Execution State\n  - [ ] Execution Output\n  - [ ] Execution Output with State\n  - [ ] Aborting Executions\n- [ ] Adhoc\n- [ ] Key Storage\n  - [ ] Upload keys\n  - [ ] List keys\n  - [ ] Get Key Metadata\n  - [ ] Get Key Contents\n  - [ ] Delete Keys\n- [ ] Projects\n  - [x] Listing Projects\n  - [x] Project Creation\n  - [x] Getting Project Info\n  - [x] Project Deletion\n  - [x] Project Configuration\n  - [x] Project Configuration Keys\n  - [ ] Project Archive Export\n  - [ ] Project Archive Export Async\n  - [ ] Project Archive Export Status\n  - [ ] Project Archive Import\n  - [ ] Updating and Listing Resources for a Project\n  - [ ] Project Readme File\n  - [ ] Project ACLs\n- [ ] Listing History\n- [ ] Resources/Nodes\n- [ ] SCM\n',
    'author': 'elda27',
    'author_email': 'kaz.birdstick@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/elda27/async_rundeck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
