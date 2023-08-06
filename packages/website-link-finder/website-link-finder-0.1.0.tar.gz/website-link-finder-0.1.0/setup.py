# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['link_finder']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'website-link-finder',
    'version': '0.1.0',
    'description': 'A python module to find all the links in a website',
    'long_description': None,
    'author': 'Mohidul Islam',
    'author_email': 'mohidul.nu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
