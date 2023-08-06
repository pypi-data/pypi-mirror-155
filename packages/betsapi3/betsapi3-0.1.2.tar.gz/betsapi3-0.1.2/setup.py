# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['betsapi3']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'betsapi3',
    'version': '0.1.2',
    'description': 'Unofficial BetsAPI wrapper for Python3',
    'long_description': '# Unofficial Python Wrapper for BetsAPI',
    'author': 'tavkhelidzeluka',
    'author_email': 'tavkhelidzeluka@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tavkhelidzeluka/betsapi3-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
