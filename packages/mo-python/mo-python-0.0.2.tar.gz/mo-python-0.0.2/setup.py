# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moalerts']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.5,<2.0.0', 'psycopg2>=2.9.3,<3.0.0']

setup_kwargs = {
    'name': 'mo-python',
    'version': '0.0.2',
    'description': 'A python package for adding alerts to the MO alerts database.',
    'long_description': None,
    'author': 'Gavin Bell',
    'author_email': 'gavin.bell@optimeering.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
