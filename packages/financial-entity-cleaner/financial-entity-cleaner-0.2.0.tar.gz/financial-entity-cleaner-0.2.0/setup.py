# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['financial_entity_cleaner',
 'financial_entity_cleaner.batch',
 'financial_entity_cleaner.country',
 'financial_entity_cleaner.id',
 'financial_entity_cleaner.text',
 'financial_entity_cleaner.utils']

package_data = \
{'': ['*'], 'financial_entity_cleaner.text': ['legal_forms/*']}

install_requires = \
['hdx-python-country==3.0.7',
 'hdx-python-utilities==3.0.7',
 'numpy>=1.16.0',
 'pandas>=1.1.5',
 'python-stdnum==1.17',
 'tqdm>=4.62.2']

entry_points = \
{'console_scripts': ['test = scripts:test']}

setup_kwargs = {
    'name': 'financial-entity-cleaner',
    'version': '0.2.0',
    'description': 'Normalization of data for entity matching',
    'long_description': "# financial-entity-cleaner\nThe financial-entity-cleaner is a library that is part of the Entity-Matching project developed by OS-Climate Foundation. The main purpose of the financial-cleaner is to provide methods for validation and standardization of data used in the banking industry as to solve the problem of determining if two entities in a data set refer to the same real-world object (entity matching).\n\nCurrently, the library provides three main components:\n- a validator for banking identifiers (Sedol,Isin and Lei),\n- a validator for country information, and \n- a cleaner for company's name.\n\n## Install from PyPi\n\n```\npip install financial-entity-cleaner\n```\n\n## How to use the library\n\nThe following jupyter notebooks teaches how to use the library:\n\n- [How to clean a company's name](https://github.com/os-climate/financial-entity-cleaner/blob/main/notebooks/how-to/Clean%20a%20company's%20name.ipynb)\n- [How to normalize country information](https://github.com/os-climate/financial-entity-cleaner/blob/main/notebooks/how-to/Normalize%20country%20information.ipynb)\n- [How to validate banking ids, such as: LEI, ISIN and SEDOL](https://github.com/os-climate/financial-entity-cleaner/blob/main/notebooks/how-to/Validate%20banking%20IDs.ipynb)\n",
    'author': 'Os-Climate Foundation',
    'author_email': 'test_os-climate@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/os-climate/financial-entity-cleaner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.11',
}


setup(**setup_kwargs)
