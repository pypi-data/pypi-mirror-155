# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docstrings']

package_data = \
{'': ['*']}

install_requires = \
['docstring-parser>=0.14.1,<0.15.0', 'hikari-crescent>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'crescent-ext-docstrings',
    'version': '0.1.0',
    'description': 'A docstring parser for hikari-crescent.',
    'long_description': None,
    'author': 'Lunarmagpie',
    'author_email': 'Bambolambo0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
