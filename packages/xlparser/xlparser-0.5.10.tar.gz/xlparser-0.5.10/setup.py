# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xlparser']
install_requires = \
['click>=8.1.3,<9.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'xlparser',
    'version': '0.5.10',
    'description': 'Parse excel(xlsx/xls/csv) to other format(csv, xlsx, json).',
    'long_description': None,
    'author': 'ahuigo',
    'author_email': '1781999+ahuigo@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
