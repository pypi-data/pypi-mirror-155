# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['traps']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.0,<3.0.0']

entry_points = \
{'console_scripts': ['traps = traps:main']}

setup_kwargs = {
    'name': 'traps',
    'version': '0.1.1',
    'description': 'how about you pip install some traps',
    'long_description': '<h1 align="center">\n  Pip Install Traps 😩\n</h1>\n\n<p align="center"> \n  <kbd>\n    <img src="https://raw.githubusercontent.com/Rdimo/images/master/pip-install-bitches/Roxy-pip-install-bitches.jpg"></img>\n  </kbd>\n</p>\n\n<p align="center">\n  <img src="https://img.shields.io/pypi/v/bitches?style=flat-square">\n  <img src="https://img.shields.io/pypi/dm/bitches?style=flat-square">\n  <img src="https://sonarcloud.io/api/project_badges/measure?project=Rdimo_pip-install-bitches&metric=ncloc">\n  <img src="https://img.shields.io/github/stars/Rdimo/pip-install-bitches?label=Stars&style=flat-square">\n  <img src="https://img.shields.io/github/forks/Rdimo/pip-install-bitches?label=Forks&style=flat-square">\n</p>\n\n<h2 align="center">\n  pip-install-bitches was made by\n\nLove ❌ code ✅\n\n</h2>\n\n---\n\n### 🎈・Code example\n\nExample of how you can use [traps](https://pypi.org/project/traps/)\n\n```python\nimport traps\n\ntraps.get()\n\n# or\n\ntraps.get(\n  "yes", # directory name (default: "traps")\n  5 # amount of traps (default: randint(5, 10))\n)\n```\n',
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
