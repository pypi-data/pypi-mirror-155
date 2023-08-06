# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gabwill10_testing', 'gabwill10_testing.core']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.9.2,<4.0.0']

setup_kwargs = {
    'name': 'gabwill10-testing',
    'version': '0.5.0',
    'description': 'first library',
    'long_description': None,
    'author': 'Gabriel Gonzalez',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
