# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fugle_trade']

package_data = \
{'': ['*']}

install_requires = \
['fugle-trade-core==0.2.5',
 'keyring==23.5.0',
 'keyrings.cryptfile==1.3.8',
 'websocket-client==1.2.1']

setup_kwargs = {
    'name': 'fugle-trade',
    'version': '0.2.6',
    'description': '',
    'long_description': None,
    'author': 'bistin',
    'author_email': 'bistin@fugle.tw',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
