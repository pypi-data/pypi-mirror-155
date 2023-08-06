# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_embrace']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.0,<8.0']

entry_points = \
{'pytest11': ['pytest_embrace = pytest_embrace.plugin']}

setup_kwargs = {
    'name': 'pytest-embrace',
    'version': '0.0.2b1',
    'description': 'Use modern Python type hints to design expressive tests. Reject boilerplate. Embrace complexity.',
    'long_description': None,
    'author': 'Ainsley McGrath',
    'author_email': 'mcgrath.ainsley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
