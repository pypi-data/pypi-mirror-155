# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forgeformat']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.3.0,<23.0.0',
 'click>=8.1.0,<9.0.0',
 'forge-core<1.0.0',
 'isort>=5.10.1,<6.0.0',
 'python-dotenv>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['forge-format = forgeformat:cli']}

setup_kwargs = {
    'name': 'forge-format',
    'version': '0.1.0',
    'description': 'Formatting library for Forge',
    'long_description': '# forge-format\n',
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
