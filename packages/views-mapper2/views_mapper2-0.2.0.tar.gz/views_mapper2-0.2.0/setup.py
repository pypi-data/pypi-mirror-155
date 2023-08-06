# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['views_mapper2']

package_data = \
{'': ['*'], 'views_mapper2': ['assets/*']}

install_requires = \
['contextily>=1.2.0',
 'geopandas>=0.9.0',
 'ingester3>=1.4.2',
 'matplotlib>=3.4.3',
 'numpy>=1.20.3',
 'pycountry>=20.7.3',
 'sqlalchemy>=1.4.29']

setup_kwargs = {
    'name': 'views-mapper2',
    'version': '0.2.0',
    'description': 'Mapper version 2 for viewser',
    'long_description': None,
    'author': 'Malika',
    'author_email': 'malikarakh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
