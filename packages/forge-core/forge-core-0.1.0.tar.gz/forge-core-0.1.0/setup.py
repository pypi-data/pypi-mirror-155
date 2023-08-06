# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forgecore']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.0,<9.0.0', 'python-dotenv>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'forge-core',
    'version': '0.1.0',
    'description': 'Core library for Forge',
    'long_description': '# forge-core\n',
    'author': 'Dave Gaeddert',
    'author_email': 'dave.gaeddert@dropseed.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.forgepackages.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
