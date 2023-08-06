# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiokeycloak',
 'aiokeycloak.authorization',
 'aiokeycloak.integrations',
 'aiokeycloak.integrations.starlette',
 'aiokeycloak.integrations.starlette.store']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'python-jose>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'aiokeycloak',
    'version': '0.0.2',
    'description': '',
    'long_description': 'None',
    'author': 'GLEF1X',
    'author_email': 'glebgar567@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
