# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forgework', 'forgework.management', 'forgework.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.0,<9.0.0',
 'forge-core<1.0.0',
 'honcho>=1.1.0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['forge-work = forgework:cli']}

setup_kwargs = {
    'name': 'forge-work',
    'version': '0.1.0',
    'description': 'Work library for Forge',
    'long_description': '# forge-work\n',
    'author': 'Dave Gaeddert',
    'author_email': 'dave.gaeddert@dropseed.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.forgepackages.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
