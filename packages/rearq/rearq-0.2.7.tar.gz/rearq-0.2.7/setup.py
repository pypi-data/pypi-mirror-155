# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rearq', 'rearq.server', 'rearq.server.routes']

package_data = \
{'': ['*'], 'rearq.server': ['static/*', 'templates/*', 'templates/widgets/*']}

install_requires = \
['aiofiles',
 'click',
 'crontab',
 'fastapi',
 'jinja2',
 'loguru',
 'pydantic',
 'redis>=4.2.0rc1,<5.0.0',
 'tortoise-orm>=0.18.1,<0.19.0',
 'uvicorn[standard]']

extras_require = \
{'mysql': ['asyncmy'], 'postgres': ['asyncpg']}

entry_points = \
{'console_scripts': ['rearq = rearq.cli:main']}

setup_kwargs = {
    'name': 'rearq',
    'version': '0.2.7',
    'description': 'Rewrite arq and make improvement.',
    'long_description': '# ReArq\n\n[![image](https://img.shields.io/pypi/v/rearq.svg?style=flat)](https://pypi.python.org/pypi/rearq)\n[![image](https://img.shields.io/github/license/long2ice/rearq)](https://github.com/long2ice/rearq)\n[![image](https://github.com/long2ice/rearq/workflows/pypi/badge.svg)](https://github.com/long2ice/rearq/actions?query=workflow:pypi)\n[![image](https://github.com/long2ice/rearq/workflows/ci/badge.svg)](https://github.com/long2ice/rearq/actions?query=workflow:ci)\n\n## Introduction\n\nReArq is a distributed task queue with asyncio and redis, which rewrite from [arq](https://github.com/samuelcolvin/arq)\nto make improvement and include web interface.\n\nYou can try [Demo Online](https://demo-rearq.long2ice.io) here.\n\n## Screenshots\n\n![dashboard](./images/dashboard.png)\n![worker](./images/worker.png)\n![task](./images/task.png)\n![job](./images/job.png)\n![result](./images/result.png)\n\n## Requirements\n\n- Redis >= 5.0\n- [TortoiseORM](https://github.com/tortoise/tortoise-orm)\n\n## Install\n\nUse MySQL backend:\n\n```shell\n> pip install rearq[mysql]\n```\n\nUse PostgreSQL backend:\n\n```shell\n> pip install rearq[postgres]\n```\n\n## Quick Start\n\n### Task Definition\n\n```python\n# main.py\nfrom rearq import ReArq\n\nrearq = ReArq(db_url=\'mysql://root:123456@127.0.0.1:3306/rearq\')\n\n\n@rearq.on_shutdown\nasync def on_shutdown():\n    # you can do some clean work here like close db and so on...\n    print("shutdown")\n\n\n@rearq.on_startup\nasync def on_startup():\n    # you should do some initialization work here\n    print("startup")\n\n\n@rearq.task(queue="q1")\nasync def add(self, a, b):\n    return a + b\n\n\n@rearq.task(cron="*/5 * * * * * *")  # run task per 5 seconds\nasync def timer(self):\n    return "timer"\n```\n\n### Run rearq worker\n\n```shell\n> rearq main:rearq worker -q q1 -q q2 # consume tasks from q1 and q2 as the same time\n```\n\n```log\n2021-03-29 09:54:50.464 | INFO     | rearq.worker:_main:95 - Start worker success with queue: rearq:queue:default\n2021-03-29 09:54:50.465 | INFO     | rearq.worker:_main:96 - Registered tasks: add, sleep, timer_add\n2021-03-29 09:54:50.465 | INFO     | rearq.worker:log_redis_info:86 - redis_version=6.2.1 mem_usage=1.43M clients_connected=5 db_keys=6\n```\n\n### Run rearq timer\n\nIf you have timing task or delay task, you should run another command also:\n\n```shell\n> rearq main:rearq timer\n```\n\n```log\n2021-03-29 09:54:43.878 | INFO     | rearq.worker:_main:275 - Start timer success\n2021-03-29 09:54:43.887 | INFO     | rearq.worker:_main:277 - Registered timer tasks: timer_add\n2021-03-29 09:54:43.894 | INFO     | rearq.worker:log_redis_info:86 - redis_version=6.2.1 mem_usage=1.25M clients_connected=2 db_keys=6\n```\n\n### Integration in FastAPI\n\n```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n\n@app.on_event("startup")\nasync def startup() -> None:\n    await rearq.init()\n\n\n@app.on_event("shutdown")\nasync def shutdown() -> None:\n    await rearq.close()\n\n\n# then run task in view\n@app.get("/test")\nasync def test():\n    job = await add.delay(args=(1, 2))\n    # or\n    job = await add.delay(kwargs={"a": 1, "b": 2})\n    # or\n    job = await add.delay(1, 2)\n    # or\n    job = await add.delay(a=1, b=2)\n    result = await job.result(timeout=5)  # wait result for 5 seconds\n    print(result.result)\n    return result\n```\n\n## Start web interface\n\n```shell\n> rearq main:rearq server\nUsage: rearq server [OPTIONS]\n\n  Start rest api server.\n\nOptions:\n  --host TEXT         Listen host.  [default: 0.0.0.0]\n  -p, --port INTEGER  Listen port.  [default: 8000]\n  -h, --help          Show this message and exit..\n```\n\nAfter server run, you can visit [https://127.0.0.1:8000/docs](https://127.0.0.1:8000/docs) to see all apis\nand [https://127.0.0.1:8000](https://127.0.0.1:8000) to see web interface.\n\n## ThanksTo\n\n- [arq](https://github.com/samuelcolvin/arq), Fast job queuing and RPC in python with asyncio and redis.\n\n## License\n\nThis project is licensed under the [Apache-2.0](./LICENSE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/rearq.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
