# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlbee']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'XlsxWriter>=3.0.3,<4.0.0',
 'about-time==3.1.1',
 'alive-progress>=2.4.1,<3.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'httpx>=0.23.0,<0.24.0',
 'icecream>=2.1.1,<3.0.0',
 'install>=1.3.5,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'set-loglevel>=0.1.2,<0.2.0',
 'tenacity>=8.0.1,<9.0.0',
 'typer>=0.4.1,<0.5.0']

extras_require = \
{'sep-text': ['sep-text>=0.1.0,<0.2.0']}

entry_points = \
{'console_scripts': ['mlbee = mlbee.__main__:app']}

setup_kwargs = {
    'name': 'mlbee',
    'version': '0.1.0a2',
    'description': 'mlbee cli: a multilingual aligner based on a machine learning model',
    'long_description': '# mlbee\n[![pytest](https://github.com/ffreemt/mlbee/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/mlbee/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/mlbee.svg)](https://badge.fury.io/py/mlbee)\n\nmlbee cli: a multilingual aligner based on a machine learning model\n\n## Install it\n\n```shell\npip install git+https://github.com/ffreemt/mlbee\n# poetry add git+https://github.com/ffreemt/mlbee-cli\n# git clone https://github.com/ffreemt/mlbee-cli && cd mlbee-cli\n```\n\n## Use it\n```python\nfrom mlbee import mlbee\n\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/mlbee-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
