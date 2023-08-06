# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyensemblorthologues', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79,<2.0',
 'fire==0.4.0',
 'mikado>=2.0,<3.0',
 'psutil>=5.8.0,<6.0.0',
 'requests']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.13.6,<0.14.0',
         'mkdocs-autorefs==0.1.1'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1']}

entry_points = \
{'console_scripts': ['pyensemblorthologues = pyensemblorthologues.cli:main']}

setup_kwargs = {
    'name': 'pyensemblorthologues',
    'version': '0.1.3',
    'description': 'Tool to download ortologue genes from ensembl compara.',
    'long_description': '# PyEnsemblOrthologues\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/pyensemblorthologues">\n    <img src="https://img.shields.io/pypi/v/pyensemblorthologues.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/homonecloco/pyensemblorthologues/actions">\n    <img src="https://github.com/homonecloco/pyensemblorthologues/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://pyensemblorthologues.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/pyensemblorthologues/badge/?version=latest" alt="Documentation Status">\n</a>\n\n</p>\n\n\nTool to download ortologue genes from ensembl compara\n\n\n* Free software: MIT\n* Documentation: <https://pyensemblorthologues.readthedocs.io>\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'Ricardo H. Ramirez-Gonzalez',
    'author_email': 'ricardo.ramirez-gonzalez@jic.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/homonecloco/pyensemblorthologues',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
