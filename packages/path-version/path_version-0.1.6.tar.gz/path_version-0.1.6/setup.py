# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['path_version']
setup_kwargs = {
    'name': 'path-version',
    'version': '0.1.6',
    'description': 'Get the last changed has of a dir as a python function',
    'long_description': '# Path Version\n\nHelper to get the git hash of the last change to a particular sub-directory\nin a repository.\n\nNeeds to be a separate package so that we can install it in the same virtualenv\nas poetry and poetry-dynamic-versioning at least until we have poetry 1.2 and\nproper poetry plugin support.\n',
    'author': 'Oxford Ionics',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
