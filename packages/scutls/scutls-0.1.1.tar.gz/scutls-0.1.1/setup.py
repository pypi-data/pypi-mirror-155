# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scutls']

package_data = \
{'': ['*'], 'scutls': ['assets/*']}

install_requires = \
['importlib-resources>=5.8.0,<6.0.0', 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['scutls = scutls.arguments:main']}

setup_kwargs = {
    'name': 'scutls',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
