# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meraki_env']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv']

setup_kwargs = {
    'name': 'meraki-env',
    'version': '0.1.4',
    'description': 'Meraki Env wrapper',
    'long_description': None,
    'author': 'Thomas Christory',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
