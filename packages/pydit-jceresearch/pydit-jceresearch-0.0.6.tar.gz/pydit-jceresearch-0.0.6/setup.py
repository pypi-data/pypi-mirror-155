# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydit', 'pydit.functions']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib',
 'myst-parser',
 'numpy>=1.21.5,<2.0.0',
 'openpyxl>=3.0.0,<4.0.0',
 'pandas>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'pydit-jceresearch',
    'version': '0.0.6',
    'description': 'Data cleansing tools for Internal Auditors',
    'long_description': None,
    'author': 'jceresearch',
    'author_email': 'jceresearch@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
