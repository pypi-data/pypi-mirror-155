# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rwthcolors', 'rwthcolors.colors']

package_data = \
{'': ['*']}

install_requires = \
['cycler>=0.11.0,<0.12.0', 'matplotlib>=3.5.2,<4.0.0', 'pytest>=7.1.1,<8.0.0']

setup_kwargs = {
    'name': 'rwthcolors',
    'version': '0.1.5',
    'description': 'Simple library that makes it easier to use RWTH CI colors in python projects',
    'long_description': '',
    'author': 'Philipp Simon Leibner',
    'author_email': 'philipp.leibner@ifs.rwth-aachen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
