# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['addrparser', 'addrparser.locales', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['pyparsing>=3.0.9,<4.0.0']

extras_require = \
{'cli': ['click>=8.1.3,<9.0.0'],
 'dev': ['pre-commit>=2.19.0,<3.0.0',
         'railroad-diagrams>=1.1.1,<2.0.0',
         'jinja2>=3.1.2,<4.0.0',
         'bump2version>=1.0.1,<2.0.0',
         'tox>=3.25.0,<4.0.0'],
 'doc': ['mkdocs>=1.3.0,<2.0.0',
         'pymdown-extensions>=9.5,<10.0',
         'mkdocs-material>=8.3.4,<9.0.0',
         'mkdocs-include-markdown-plugin>=3.5.2,<4.0.0',
         'mkdocstrings[python]>=0.19.0,<0.20.0',
         'mkdocs-autorefs>=0.4.1,<0.5.0'],
 'test': ['click>=8.1.3,<9.0.0',
          'black>=22.3.0,<23.0.0',
          'isort>=5.10.1,<6.0.0',
          'mypy>=0.961,<0.962',
          'flake8<4.0.0',
          'pytest>=7.1.2,<8.0.0',
          'pytest-cov>=3.0.0,<4.0.0']}

entry_points = \
{'console_scripts': ['addr-parse = addrparser.cli:main']}

setup_kwargs = {
    'name': 'addrparser',
    'version': '0.1.0',
    'description': 'Address parser for Finnish addresses',
    'long_description': '# Address parser\n\n[![pypi](https://img.shields.io/pypi/v/addrparser.svg)](https://pypi.org/project/addrparser/)\n[![python](https://img.shields.io/pypi/pyversions/addrparser.svg)](https://pypi.org/project/addrparser/)\n[![Build Status](https://github.com/gispocoding/addr-parser/actions/workflows/dev.yml/badge.svg)](https://github.com/gispocoding/addr-parser/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/gispocoding/addr-parser/branch/main/graphs/badge.svg)](https://codecov.io/github/gispocoding/addr-parser)\n\nSimple address parser with localization support.\n\n> **Note:**\n> This library is meant to be simple, light weight and easy to adapt. This is not the best and most optimized address parser out there.\n> For *state of the art* parser you should probably look at https://github.com/openvenues/pypostal\n\n* Documentation: <https://gispocoding.github.io/addr-parser>\n* GitHub: <https://github.com/gispocoding/addr-parser>\n* PyPI: <https://pypi.org/project/addrparser/>\n* Free software: MIT\n\n## Supported countries\n| Country         | Description                            | Documentation                                          |\n| --------------- | -------------------------------------- | ------------------------------------------------------ |\n| Suomi - Finland | Suomalaisten osoitteiden osoiteparseri | <https://gispocoding.github.io/addr-parser/locales/fi> |\n\n## Installation\n\n```\npip install addrparser\n```\n\n### Setting up a development environment\nSee instructions in [CONTRIBUTING.md](./CONTRIBUTING.md#get-started)\n\n## Usage\n\n### Command line tool\n```shell\n$ addr-parse --help\nUsage: addr-parse [OPTIONS] ADDRESS\n\n  Cli tool for parsing text addresses.\n\n  Args:     address (str): address text\n\nOptions:\n  -l, --locale TEXT  Country code in two-letter ISO 3166\n  --help             Show this message and exit.\n```\n\n```shell\n$ addr-parser "Iso Maantie 12b B 7"\n{\n  "input": "Iso Maantie 12b B 7",\n  "result": {\n    "street_name": "Iso Maantie",\n    "house_number": "12b",\n    "entrance": "B",\n    "apartment": "7"\n  }\n}\n```\n### Library\n```python\n>>> from addrparser import AddressParser\n\n>>> parser = AddressParser(\'fi\')\n>>> address = parser.parse(\'Iso Maantie 12b B 7\')\n>>> address\nAddress(street_name=\'Iso Maantie\', house_number=\'12b\', entrance=\'B\', apartment=\'7\', post_office_box=None, zip_number=None, zip_name=None)\n```\n\n## Credits\n\nThis project was created with inspiration from [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Lauri Kajan',
    'author_email': 'lauri.kajan@gispo.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
