# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataobjtools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dataobjtools',
    'version': '0.1.3',
    'description': 'Data Object helpers for Dicts and Lists for searching, managing,  manipulating etc',
    'long_description': None,
    'author': 'pub12',
    'author_email': 'pubudu79@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
