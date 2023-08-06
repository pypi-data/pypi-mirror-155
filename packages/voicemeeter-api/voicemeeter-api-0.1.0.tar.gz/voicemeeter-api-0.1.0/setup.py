# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['voicemeeterlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'voicemeeter-api',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'onyx-and-iris',
    'author_email': 'code@onyxandiris.online',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
