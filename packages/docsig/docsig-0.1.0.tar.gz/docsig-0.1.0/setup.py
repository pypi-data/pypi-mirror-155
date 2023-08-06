# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docsig']

package_data = \
{'': ['*']}

install_requires = \
['object-colors>=2.1.0,<3.0.0']

entry_points = \
{'console_scripts': ['docsig = docsig.__main__:main']}

setup_kwargs = {
    'name': 'docsig',
    'version': '0.1.0',
    'description': 'Check signature params for proper documentation',
    'long_description': 'docsig\n======\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n    :alt: License\n.. image:: https://img.shields.io/pypi/v/docsig\n    :target: https://img.shields.io/pypi/v/docsig\n    :alt: pypi\n.. image:: https://github.com/jshwi/docsig/actions/workflows/ci.yml/badge.svg\n    :target: https://github.com/jshwi/docsig/actions/workflows/ci.yml\n    :alt: CI\n.. image:: https://codecov.io/gh/jshwi/docsig/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/docsig\n    :alt: codecov.io\n.. image:: https://readthedocs.org/projects/docsig/badge/?version=latest\n    :target: https://docsig.readthedocs.io/en/latest/?badge=latest\n    :alt: readthedocs.org\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nCheck signature params for proper documentation\n-----------------------------------------------\n\nInstallation\n------------\n\n.. code-block:: console\n\n    $ pip install docsig\n\nUsage\n-----\n\nCommandline\n***********\n\n.. code-block:: console\n\n    usage: docsig [-h] [-c INT] [-l INT] [-s STR] [-i LIST] [-I LIST]usage: docsig [-h] [-v] path\n\n    Check docstring matches signature\n\n    positional arguments:\n      path           directory or file to check\n\n    optional arguments:\n      -h, --help     show this help message and exit\n      -v, --version  show version and exit\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': 'jshwi',
    'maintainer_email': 'stephen@jshwisolutions.com',
    'url': 'https://pypi.org/project/docsig/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
