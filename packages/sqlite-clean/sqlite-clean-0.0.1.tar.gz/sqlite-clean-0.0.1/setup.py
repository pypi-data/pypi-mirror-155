# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlite_clean']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.37,<2.0.0']

setup_kwargs = {
    'name': 'sqlite-clean',
    'version': '0.0.1',
    'description': 'A SQLite data validation and cleanup tool.',
    'long_description': None,
    'author': 'd33bs',
    'author_email': 'dave.bunten@cuanschutz.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
