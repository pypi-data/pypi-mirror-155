# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['misery']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'misery',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Anton Evdokimov',
    'author_email': 'meowmeowcode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
