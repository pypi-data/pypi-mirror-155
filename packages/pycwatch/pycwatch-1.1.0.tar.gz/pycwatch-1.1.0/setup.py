# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycwatch']

package_data = \
{'': ['*']}

install_requires = \
['api-client-pydantic>=2.0.0,<3.0.0',
 'api-client>=1.3.1,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pycwatch',
    'version': '1.1.0',
    'description': 'An client library for the Cryptowatch Rest API.',
    'long_description': '# pycwatch\n\n[![Coverage](https://img.shields.io/codecov/c/github/ljnsn/pycwatch?color=%2334D058)](https://codecov.io/gh/ljnsn/pycwatch)\n[![Package version](https://img.shields.io/pypi/v/pycwatch?color=%2334D058&label=pypi%20package)](https://pypi.org/project/pycwatch)\n[![Python versions](https://img.shields.io/pypi/pyversions/pycwatch.svg)](https://pypi.org/project/pycwatch)\n[![Black style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nThe `pycwatch` library provides access to the [Cryptowatch API](https://docs.cryptowat.ch/rest-api/) and implements all resources of the REST API.\n\n## Installation\n\nEither install from pypi or clone this repository and install locally.\n\n```fish\npip install pycwatch\n```\n\n## Quick Start\n\nSee the [cryptowat.ch docs](https://docs.cryptowat.ch/rest-api) for available endpoints.\n\n```python\nfrom pycwatch import CryptoWatchClient\n\n# create api client\nclient = CryptoWatchClient()\n\n# get list of available assets\nassets = client.list_assets()\n# get some price info\nexchange, pair = "binance", "btceur"\nprice = client.get_market_price(exchange, pair)\n```\n\nIf you have an account at [cryptowat.ch](https://cryptowat.ch), you can either set your key as an environment variable or in the code.\n\n```bash\nexport CRYPTO_WATCH_KEY="my-awesome-key"\n```\n\nor\n\n```python\nfrom pycwatch import CryptoWatchClient\n\napi_key = "my-awesome-key"\nclient = CryptoWatchClient(api_key)\n```\n',
    'author': 'ljnsn',
    'author_email': '82611987+ljnsn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ljnsn/pycwatch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
