# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google_address_to_latlong_csv']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'google-address-to-latlong-csv',
    'version': '0.1.0',
    'description': 'This is an Python 3 Program which gets the list of data of addresses from an csv file and gives an output as csv with additional fields of latitude and longitude of the address provided by google GeoCoding API.',
    'long_description': None,
    'author': 'Shrikant Dhayje',
    'author_email': 'shrikantdhayaje@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
