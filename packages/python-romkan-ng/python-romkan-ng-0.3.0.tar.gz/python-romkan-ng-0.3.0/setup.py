# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['romkan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-romkan-ng',
    'version': '0.3.0',
    'description': 'A Romaji/Kana conversion library',
    'long_description': None,
    'author': 'Augustin Cisterne-Kaas',
    'author_email': 'ajitekun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
