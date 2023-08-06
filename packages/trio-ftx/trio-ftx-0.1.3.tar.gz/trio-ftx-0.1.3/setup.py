# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trio_ftx']

package_data = \
{'': ['*']}

install_requires = \
['ciso8601>=2.2.0,<3.0.0',
 'httpx>0.20.0',
 'trio-websocket>=0.9.2,<0.10.0',
 'trio>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'trio-ftx',
    'version': '0.1.3',
    'description': 'Trio powered FTX async python client',
    'long_description': None,
    'author': 'Shu Wang',
    'author_email': 'halfelf.ronin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
