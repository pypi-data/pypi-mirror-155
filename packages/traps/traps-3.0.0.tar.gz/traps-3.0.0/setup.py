# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['traps']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'loguru>=0.6.0,<0.7.0', 'requests>=2.28.0,<3.0.0']

entry_points = \
{'console_scripts': ['traps = traps.cli:main']}

setup_kwargs = {
    'name': 'traps',
    'version': '3.0.0',
    'description': 'How about you pip install some traps?',
    'long_description': '<h1 align="center">\n  Pip Install Traps 😩\n</h1>\n\n<p align="center"> \n  <kbd>\n    <img src="https://raw.githubusercontent.com/analgadgets/pip-install-traps/main/images/trap.jpg">\n  </kbd>\n</p>\n\n<p align="center">\n  <img src="https://img.shields.io/pypi/v/traps?style=flat-square">\n  <img src="https://img.shields.io/github/stars/analgadgets/pip-install-traps?label=Stars&style=flat-square">\n  <img src="https://img.shields.io/github/forks/analgadgets/pip-install-traps?label=Forks&style=flat-square">\n</p>\n\n<h2 align="center">\n  pip-install-traps was made with\n\nCum ❌ code ✅\n\n</h2>\n\n---\n\n### Installation\n```\npip install -U traps\n```\n\n### Usage\n```python\nimport traps\n\ntraps.get()  # Download one trap to `traps` directory.\ntraps.get("my_homework", 15)  # Or download 15 traps to another directory.\n```\n\n### Command-line interface\n* `$ traps install` to download 10 traps to `traps` directory\n* `$ traps install -n 20 my_homework` to download 20 traps to `my_homework` directory\n* `$ traps --help` for more help\n',
    'author': 'Rdimo',
    'author_email': 'contact.rdimo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
