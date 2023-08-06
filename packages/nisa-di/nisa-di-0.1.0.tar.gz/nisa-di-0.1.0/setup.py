# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nisa_di']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nisa-di',
    'version': '0.1.0',
    'description': 'nisa dependencies injection pure python',
    'long_description': None,
    'author': 'vaziria',
    'author_email': 'manorder123@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
