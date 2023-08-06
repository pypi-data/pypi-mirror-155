# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bee_utils']

package_data = \
{'': ['*']}

install_requires = \
['icecream>=2.1.1,<3.0.0',
 'install>=1.3.5,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'set-loglevel>=0.1.2,<0.2.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['bee-utils = bee_utils.__main__:app']}

setup_kwargs = {
    'name': 'bee-utils',
    'version': '0.1.0a0',
    'description': 'Various util functions for the bee family and other uses',
    'long_description': '# bee-utils\n[![pytest](https://github.com/ffreemt/bee-utils/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/bee-utils/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/bee_utils.svg)](https://badge.fury.io/py/bee_utils)\n\nVarious util functions for the bee family and other uses\n\n## Install it\n\n```shell\npip install git+https://github.com/ffreemt/bee-utils\n# poetry add git+https://github.com/ffreemt/bee-utils\n# git clone https://github.com/ffreemt/bee-utils && cd bee-utils\n```\n\n## Use it\n```python\nfrom bee_utils import bee_utils\n\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/bee-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
