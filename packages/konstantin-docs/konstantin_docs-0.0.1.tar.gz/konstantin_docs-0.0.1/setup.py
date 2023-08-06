# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['konstantin_docs']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.28.0']

setup_kwargs = {
    'name': 'konstantin-docs',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Konstantin-Dudersky',
    'author_email': 'Konstantin.Dudersky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
