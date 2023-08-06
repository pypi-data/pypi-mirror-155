# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycsbinarywriter', 'pycsbinarywriter.cstypes', 'pycsbinarywriter.test']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2022.1,<2023.0']

setup_kwargs = {
    'name': 'pycsbinarywriter',
    'version': '0.0.2',
    'description': 'Helpers for parsing binary data created by dotnet BinaryWriters.',
    'long_description': None,
    'author': 'Rob Nelson',
    'author_email': 'nexisentertainment@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
