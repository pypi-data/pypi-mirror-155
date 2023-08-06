# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forgetailwind']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.0,<9.0.0', 'forge-core<1.0.0', 'requests>=2.28.0,<3.0.0']

entry_points = \
{'console_scripts': ['forge-tailwind = forgetailwind:cli']}

setup_kwargs = {
    'name': 'forge-tailwind',
    'version': '0.1.0',
    'description': 'Work library for Forge',
    'long_description': '# forge-tailwind\n',
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
