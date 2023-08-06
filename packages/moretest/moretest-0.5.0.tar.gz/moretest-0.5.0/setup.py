# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moretest']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['APPLICATION-NAME = entry:main']}

setup_kwargs = {
    'name': 'moretest',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'chrbrauer',
    'author_email': 'christoph@5xbrauer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
