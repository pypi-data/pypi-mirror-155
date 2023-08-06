# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_connectors']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.37,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pygsheets>=2.0.5,<3.0.0',
 'pyodbc>=4.0.32,<5.0.0',
 'python-dotenv>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'data-connectors',
    'version': '0.20.3',
    'description': '',
    'long_description': None,
    'author': 'CA Lee',
    'author_email': 'flowstate_crypto@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
