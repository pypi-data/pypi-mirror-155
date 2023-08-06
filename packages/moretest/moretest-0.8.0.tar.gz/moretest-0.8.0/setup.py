# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moretest']

package_data = \
{'': ['*']}

install_requires = \
['inquirer>=0.1,<0.2']

entry_points = \
{'console_scripts': ['APPLICATION-NAME = moretest.entry:main']}

setup_kwargs = {
    'name': 'moretest',
    'version': '0.8.0',
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
