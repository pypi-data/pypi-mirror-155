# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytiktok', 'pytiktok.models']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0', 'requests>=2.24,<3.0']

setup_kwargs = {
    'name': 'python-tiktok',
    'version': '0.1.1',
    'description': 'A simple Python wrapper for Tiktok API. ✨ 🍰 ✨',
    'long_description': 'python-tiktok\n\nA simple Python wrapper around for Tiktok API :sparkles: :cake: :sparkles:.\n\n',
    'author': 'ikaroskun',
    'author_email': 'merle.liukun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sns-sdks/python-tiktok',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
