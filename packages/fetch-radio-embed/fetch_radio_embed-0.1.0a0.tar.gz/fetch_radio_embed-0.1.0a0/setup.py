# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fetch_radio_embed']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0',
 'icecream>=2.1.1,<3.0.0',
 'install>=1.3.5,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'set-loglevel>=0.1.2,<0.2.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['fetch-radio-embed = fetch_radio_embed.__main__:app']}

setup_kwargs = {
    'name': 'fetch-radio-embed',
    'version': '0.1.0a0',
    'description': 'fetch embeding from hf radio-embed',
    'long_description': '# fetch-radio-embed\n[![pytest](https://github.com/ffreemt/fetch-radio-embed/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/fetch-radio-embed/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/fetch_radio_embed.svg)](https://badge.fury.io/py/fetch_radio_embed)\n\nFetch embedding from hf radio-embed\n\n## Install it\n\n```shell\npip install git+https://github.com/ffreemt/fetch-radio-embed\n# poetry add git+https://github.com/ffreemt/fetch-radio-embed\n# git clone https://github.com/ffreemt/fetch-radio-embed && cd fetch-radio-embed\n```\n\n## Use it\n```python\nfrom fetch_radio_embed import fetch_radio_embed\n\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/fetch-radio-embed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
