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
    'version': '0.1.0',
    'description': 'how about you pip install some traps',
    'long_description': None,
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
