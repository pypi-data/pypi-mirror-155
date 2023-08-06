# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spraymistf638']

package_data = \
{'': ['*']}

install_requires = \
['bluepy>=1.3.0']

setup_kwargs = {
    'name': 'spraymistf638',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Python Library for controlling of Spray-Mist-F638\n\n![test](https://github.com/paulokow/Spray-Mist-F638-driver-bluepy/workflows/test/badge.svg?branch=master)\n[![codecov](https://codecov.io/gh/paulokow/Spray-Mist-F638-driver-bluepy/branch/master/graph/badge.svg)](https://codecov.io/gh/paulokow/Spray-Mist-F638-driver-bluepy)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## Usage example\n\n```python\nfrom spraymistf638.driver import (\n  SprayMistF638,\n  WorkingMode,\n  RunningMode,\n  SprayMistF638Exception\n)\n\ndevice = SprayMistF638("11:11:11:11:11:11")\nif device.connect():\n  work_mode = device.working_mode\n  run_mode = device.running_mode\n  device.disconnect()\n```\n',
    'author': 'Pawel Kowalik',
    'author_email': 'github-pub@paulonet.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/paulokow/Spray-Mist-F638-driver-bluepy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
