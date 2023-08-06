# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['more_cli']

package_data = \
{'': ['*']}

install_requires = \
['inquirer', 'pick', 'pyfiglet', 'requests']

entry_points = \
{'console_scripts': ['more = more_cli.main:main']}

setup_kwargs = {
    'name': 'more-cli',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'chrbrauer',
    'author_email': 'christoph@5xbrauer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
