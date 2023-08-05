# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipython_pygments']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.0']

setup_kwargs = {
    'name': 'ipython-pygments',
    'version': '0.1.0',
    'description': 'Syntax highlighting for ipython',
    'long_description': None,
    'author': 'Thomas MK',
    'author_email': 'tmke@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
