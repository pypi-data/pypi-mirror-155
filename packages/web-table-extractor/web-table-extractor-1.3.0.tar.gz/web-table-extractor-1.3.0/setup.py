# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['table_extractor', 'table_extractor.models']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'html5lib>=1.1,<2.0',
 'requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'web-table-extractor',
    'version': '1.3.0',
    'description': 'Extract tables from HTML',
    'long_description': None,
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
