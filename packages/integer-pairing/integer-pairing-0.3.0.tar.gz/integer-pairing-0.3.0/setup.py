# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['integer_pairing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'integer-pairing',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Nejc Ševerkar',
    'author_email': 'nseverkar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kuco23/integer-pairing/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
