# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odin_messages']

package_data = \
{'': ['*']}

install_requires = \
['autopep8>=1.6.0,<2.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'odin-messages',
    'version': '0.5.1',
    'description': '',
    'long_description': None,
    'author': 'adolfrodeno',
    'author_email': 'amvillalobos@uc.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
