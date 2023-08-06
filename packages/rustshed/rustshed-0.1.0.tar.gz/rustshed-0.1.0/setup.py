# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rustshed']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rustshed',
    'version': '0.1.0',
    'description': 'Rust types in Python.',
    'long_description': None,
    'author': 'Paweł Rubin',
    'author_email': 'pawelrubindev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
