# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['summon_python']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0']

extras_require = \
{'core': ['summon-tasks>=0.2.0,<0.3.0']}

entry_points = \
{'summon': ['summon_python = summon_python.plugin']}

setup_kwargs = {
    'name': 'summon-python',
    'version': '0.2.0',
    'description': 'A collection of Python project-related tasks for Summon.',
    'long_description': None,
    'author': 'Tarcísio Eduardo Moreira Crocomo',
    'author_email': 'tarcisioe@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
