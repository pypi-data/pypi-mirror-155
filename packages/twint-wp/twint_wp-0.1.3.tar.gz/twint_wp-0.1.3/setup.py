# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twint_wp', 'twint_wp.storage']

package_data = \
{'': ['*']}

install_requires = \
['PySocks>=1.7.1,<2.0.0',
 'aiodns>=3.0.0,<4.0.0',
 'aiohttp-socks<=0.4.1',
 'aiohttp>=3.7.0,<4.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'elasticsearch>=7.16.2,<8.0.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'geopy>=2.2.0,<3.0.0',
 'googletransx>=2.4.2,<3.0.0',
 'schedule>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'twint-wp',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'coso',
    'author_email': 'cosocosa627@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
