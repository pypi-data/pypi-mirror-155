# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['entry']
entry_points = \
{'console_scripts': ['APPLICATION-NAME = entry:main']}

setup_kwargs = {
    'name': 'moretest',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'chrbrauer',
    'author_email': 'christoph@5xbrauer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
