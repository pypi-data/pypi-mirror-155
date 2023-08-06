# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryptobeacon',
 'cryptobeacon.assets',
 'cryptobeacon.commands',
 'cryptobeacon.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.0,<3.0.0', 'rich>=12.4.4,<13.0.0', 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['cryptobeacon = cryptobeacon.main:app']}

setup_kwargs = {
    'name': 'cryptobeacon',
    'version': '1.0.1',
    'description': 'CryptoBeacon is a simple command-line interface tool for cryptocurrency alerts directly into your desktop.',
    'long_description': '# 🚨 CryptoBeacon\n\n[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)\n[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)\n\nCryptoBeacon is a simple command-line interface tool for cryptocurrency alerts directly into your desktop. It uses the free [CoinGecko API](https://www.coingecko.com/en/api/documentation) to obtain the current prices, sending desktop notification when alarm price targets are reached. The application is built in [Python](https://www.python.org/), with the help of [Typer](https://github.com/tiangolo/typer) and [Rich](https://github.com/Textualize/rich).\n\n![watchlist](./imgs/watchlist.png)\n\n## Installation\n\n```Bash\npip install --user cryptobeacon\n```\n\n## Usage\n\nTracking your favorite cryptocurrencies with **CryptoBeacon** is easy. Start by **adding** them to the watchlist, as follows:\n\n```Bash\ncryptobeacon coin add bitcoin\n```\n\nConfirm the addition using the **show** command:\n\n```Bash\ncryptobeacon show\n```\n\nNext, you need to add a price target for the **alarm**:\n\n```Bash\ncryptobeacon alarm add bitcoin 21000\n```\n\nFinally, **run** the application:\n\n```Bash\ncryptobeacon run\n```\n\n> ⚠️ Additionally, there are commands to **remove** coins and alarms from the watchlist, or even to **clear** it entirely. Use the **help** commando for more specific information.\n',
    'author': 'Eduardo V. e Sousa',
    'author_email': 'eduardoatrcomp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
