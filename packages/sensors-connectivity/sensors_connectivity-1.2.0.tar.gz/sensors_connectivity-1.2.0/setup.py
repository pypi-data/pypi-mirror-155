# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['connectivity',
 'connectivity.config',
 'connectivity.src.drivers',
 'connectivity.src.feeders',
 'connectivity.src.stations',
 'connectivity.utils']

package_data = \
{'': ['*']}

install_requires = \
['ipfshttpclient==0.8.0a2',
 'netifaces>=0.11.0,<0.12.0',
 'paho-mqtt>=1.6.1,<2.0.0',
 'pinatapy-vourhey>=0.1.3,<0.2.0',
 'prometheus-client>=0.13.1,<0.14.0',
 'pynacl>=1.5.0,<2.0.0',
 'pyserial>=3.5,<4.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.27.1,<3.0.0',
 'robonomics-interface>=0.5.3,<0.6.0',
 'sentry_sdk>=1.1.5,<2.0.0']

entry_points = \
{'console_scripts': ['sensors_connectivity = connectivity.main:run']}

setup_kwargs = {
    'name': 'sensors-connectivity',
    'version': '1.2.0',
    'description': 'Robonomics package to read data from sensors and publish to different output channels',
    'long_description': '# Add telemetry agent functions to your Aira instance\nAira source package to input data from sensors.\n\n# Module For Your Aira Instance. Add Telemetry Agent\n\nThe Aira package allows you to read data from a SDS011 sensor (and a few others) and publish to different output channels.\nThat said Aira is able to form Demand and Result messages and a few other channels.\nAlso it includes Datalog feature which is still experimental. It could be used to publish data to Substrate based blockchain by [Robonomics](https://parachain.robonomics.network/).\n\n## Pre-requirements\n\nTo build a python package IPFS daemon should be installed. Assyming, you work with linux:\n\n```\nwget https://dist.ipfs.io/go-ipfs/v0.8.0/go-ipfs_v0.8.0_linux-amd64.tar.gz\ntar -xzf go-ipfs_v0.8.0_linux-amd64.tar.gz\ncd go-ipfs\nsudo bash install.sh \nipfs init\n```\n\n# Installation as PyPi package\n\n```\npip3 install py-sr25519-bindings\npip3 install sensors-connectivity\n```\n\n## Configuration\n\n[Here](https://wiki.robonomics.network/docs/configuration-options-description/) you can find an article to set a proper configuration for your instance.\n\n## Running\n\nFirst, launch IPFS daemon:\n\n```\nipfs daemon --enable-pubsub-experiment\n```\nAfter config and log files are setted, you can run the service: (in another terminal)\n\n```\nsensors_connectivity "path/to/your/config/file"\n```\n\nYou will be able to see logs in your console and in `~/.logs`.\n\n# Build from source\n## Requirements\n\nTo build a python package fron source [poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) should be also installed. Assyming, you work with linux:\n\n```\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\n\n## Get a Package And Installing dependencies\n\n```\ngit clone https://github.com/airalab/sensors-connectivity\ncd sensors-connectivity\npoetry install\n```\n\n## Documentation\n\nTo prepare a sensor for the work with the package follow instructions on [Robonomics Wiki](https://wiki.robonomics.network/docs/connect-sensor-to-robonomics/).\n\n## Configuration\n\n[Here](https://wiki.robonomics.network/docs/configuration-options-description/) you can find an article to set a proper configuration for your instance.\n\nMake a copy of `default.json` and fill it using description from the article.\n\nYou also can set a logging file. The default file for logs is `logging.py`, which uses `console` and `file` handler by default. Pay attention for the `file` handler. The template is stored in `connectivity/config/logging_template.py`. You can cpecify the path (`filename`), where your logs will be stored in (do not forget to create this directory if it doesn\'t exist). Default path for logs is `~/.logs`. You can figure any other handlers from the [library](https://docs.python.org/3.8/library/logging.html).\n\n## Running\n\nFirst, launch IPFS daemon:\n\n```\nipfs daemon --enable-pubsub-experiment\n```\nAfter config and log files are setted, you can run the service: (in another terminal)\n\n```\npoetry run sensors_connectivity "path/to/your/config/file"  \n```\n\nIf your log file is setted with `console` handler, you will be able to see logs in your console.\n\nExample of output:\n\n```\n2022-02-17 19:30:51,248 - INFO - Getting data from the stations...\n2022-02-17 19:30:51,443 - INFO - airalab-http-v0.8.0: [[], [{MAC: c8e2650f254e, Uptime: 0:00:14.010502, M: {Public: 0be87b58e87599a85dc79bf14731cc9ad547411e9b10c883e29f78fc2c67206a, geo: (53.518475,49.397178000000004), measurements: {\'airtemp\': -8.0, \'windang\': 45.0, \'windspeed\': 0.13, \'windspeedmax\': 0.13, \'pm10\': \'\', \'pm25\': \'\', \'timestamp\': 1645113602.0}}}]]\n2022-02-17 19:30:51,443 - INFO - Sending result to the feeders...\n2022-02-17 19:31:07,517 - INFO - Frontier Datalog: Data sent to Robonomics datalog and included in block 0x04baf3d81c6d31ec6f3ca3e515b9a6920666ee17cbd66f57130eaa000bad2cd4\n2022-02-17 19:31:07,519 - INFO - RobonomicsFeeder: {"0be87b58e87599a85dc79bf14731cc9ad547411e9b10c883e29f78fc2c67206a": {"model": 2, "geo": "53.518475,49.397178000000004", "measurement": {"airtemp": -8.0, "windang": 45.0, "windspeed": 0.13, "windspeedmax": 0.13, "pm10": "", "pm25": "", "timestamp": 1645113602.0}}}\n2022-02-17 19:31:07,523 - INFO - Checking data base...\n127.0.0.1 - - [17/Feb/2022 19:31:13] "POST / HTTP/1.1" 200 -\n2022-02-17 19:31:21,248 - INFO - Getting data from the stations...\n2022-02-17 19:31:21,429 - INFO - airalab-http-v0.8.0: [[{MAC: c8e2650f254e, Uptime: 0:00:43.818101, M: {Public: 133b761496539ab5d1140e94f644e2ef92c7ac32446dc782bfe1a768379a669a, geo: (1,200), measurements: {\'pm10\': 27.58, \'pm25\': 15.02, \'temperature\': 22.93, \'pressure\': 758.0687068706872, \'humidity\': 39.44, \'timestamp\': 1645115473}}}], [{MAC: c8e2650f254e, Uptime: 0:00:43.996539, M: {Public: 0be87b58e87599a85dc79bf14731cc9ad547411e9b10c883e29f78fc2c67206a, geo: (53.518475,49.397178000000004), measurements: {\'airtemp\': -8.0, \'windang\': 45.0, \'windspeed\': 0.13, \'windspeedmax\': 0.13, \'pm10\': \'\', \'pm25\': \'\', \'timestamp\': 1645113602.0}}}]]\n2022-02-17 19:31:21,444 - INFO - Sending result to the feeders...\n2022-02-17 19:31:51,249 - INFO - Getting data from the stations...\n```\n\n## Troubleshooting\n\n### Python.h: No such file or directory\n\nIf during running `poetry install` comand you get such error, you need to install the header files and static libraries for python dev. Use your package manager for installation. For example, for `apt` you need to run\n```\nsudo apt install python3-dev\n```\n> Note:\npython3-dev does not cover all versions for python3. The service needs at least python3.8, for that you may need to specify the version `sudo apt install python3.8-dev`.\n\n[Here](https://stackoverflow.com/a/21530768) you can find examples for other package managers.\n\n### Python versions mismatch\n\nIf during running `poetry install` comand you get `SolverProblemError`, which says "The current project\'s Python requirement (3.6.9) is not compatible with some of the required packages Python requirement:..", even though you have older version of python (e.g. python3.8), you may need to specify the python version poetry is using:\n\n```\npoetry env use python3.8\n```\n',
    'author': 'Vadim Manaenko',
    'author_email': 'vadim.razorq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/airalab/sensors-connectivity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
