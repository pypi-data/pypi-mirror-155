# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dilivia_data_client', 'dilivia_data_client.connexion']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.1,<2.0.0',
 'pandas==1.4.0',
 'pydruid>=0.6.2,<0.7.0',
 'pylint>=2.12.2,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2021.3,<2022.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'dilivia-data-client',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'dilivia.enovea',
    'author_email': 'contact@dilivia.net',
    'maintainer': 'martin.nivon',
    'maintainer_email': 'martin.nivon@enovea.net',
    'url': 'https://www.dilivia.net/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
