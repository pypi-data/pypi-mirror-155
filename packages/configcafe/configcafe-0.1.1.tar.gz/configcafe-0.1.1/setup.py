# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['configcafe']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.4.4,<13.0.0']

setup_kwargs = {
    'name': 'configcafe',
    'version': '0.1.1',
    'description': 'Welcome to the config cafe!',
    'long_description': None,
    'author': "J 'Indi' Harrington",
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
