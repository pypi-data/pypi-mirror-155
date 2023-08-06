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
    'version': '0.1.2',
    'description': 'This is an Python 3 Program which gets the list of data of addresses from an csv file and gives an output as csv with additional fields of latitude and longitude of the address provided by google GeoCoding API.',
    'long_description': '# google_address_to_latlong_csv\n\n## What it does\n\nThis is a Python 3 Package which gets the list of data of addresses from an csv file and gives an output as csv with additional fields of latitude and longitude of the address provided by google GeoCoding API.\n\n## Requirements\n\n- Python 3 Installed\n- Have Google API Key of `Google GeoCoding API` You can get it from Google Cloud Console\n\n\n## Same Package for venv, pipenv and poetry\n\n## Sample Input CSV File\n\n```csv\nID,Address\n1,"Nehru Nagar, Pimpri, Pune, Opp Sheetal Hotel, Pune, 411018"\n2,"Rahatani Main Road, Rahatani, Pune, Near Baliraj Garden, Pune, 411017"\n3,"Chinchwad East, Pune, Near Thermax Chowk, Pune, 411019"\n4,"Shop No 7/61/2, Tapavan Road, Pimpri Gaon-Pimpri, Pune, Near Tapavan, Pune, 411018"\n5,"Chinchwad, Pune, Near Post Office Chaphekar Chowk, Pune, 411033"\n6,"Pune, Maharashtra, India, Pune, 411038"\n7,"New Sanghvi Rd, Sangavi, Pune, Near Famous Chowk, Pune, 411027"\n8,"Moshi, Pune, Nageshwar Nagar, Pune, 412105"\n9,"Near Chintamani Chowk, Pune, 411035"\n10,"Nigdi, Pune, Next Om Swadish Bhel, Pune, 411044"\n```\n\n## How to use the Package\n\nJust Install with `pip install google-address-to-latlong-csv`\n\nAnd in your Python Program run Given Below Commands\n\n```python\nfrom google_address_to_latlong_csv import AddressToLatLong\n\napp = AddressToLatLong(input_csv_file="input.csv", output_csv_file="output.csv", google_api_key="google_api_key")\n\napp.run()\n```\n\nthe variable name `app` is not mandatory you can give any name to variable\n\nIf Any Issues occured raise `GitHub Issue on` [issues](https://github.com/shriekdj/google_address_to_latlong_csv) or Contact Me via mail me.\n\nMy Name Is **Shrikant Dhayje**.\nMy GitHub Username Is **[shriekdj](https://github.com/shriekdj)**.\nMy Official Email Id Is [shrikantdhayaje@gmail.com](mailto:shrikantdhayaje@gmail.com)\n\nI Will Try to Give Response Within 24 Hours.\n',
    'author': 'Shrikant Dhayje',
    'author_email': 'shrikantdhayaje@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shriekdj/google_address_to_latlong_csv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
