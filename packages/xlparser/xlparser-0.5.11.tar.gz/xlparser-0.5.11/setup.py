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
    'version': '0.5.11',
    'description': 'Parse excel(xlsx/xls/csv) to other format(csv, xlsx, json).',
    'long_description': '- [xlparser](#xlparser)\n  - [Install](#install)\n  - [Usage](#usage)\n    - [CLI Usage](#cli-usage)\n    - [Module Usage](#module-usage)\n    - [Parse any type of file](#parse-any-type-of-file)\n    - [Save to any type of file](#save-to-any-type-of-file)\n    - [Csv operation](#csv-operation)\n    - [Zip operation](#zip-operation)\n  - [Required](#required)\n\n# xlparser\nParse excel(xlsx/xls/csv) to other format(csv, xlsx, json).\n\n\n[![](https://img.shields.io/pypi/pyversions/xlparser.svg?longCache=True)](https://pypi.org/pypi/xlparser/)\n[![](https://img.shields.io/pypi/v/xlparser.svg?maxAge=36000)](https://pypi.org/pypi/xlparser/)\n\n## Install\n\n    pip install xlparser\n    # or\n    pip3 install xlparser\n\nIf you want to filter fields, it will be convenient with [xcut](https://github.com/ahuigo/xcut).\n\n    pip install xcut \n    # or\n    pip3 install xcut \n\n## Usage\n\n    $ xlparser -h\n    xlparser [options] INFILE [OUTFILE]\\n\n        options:\\n\n            -h       For help.\\n\n\n### CLI Usage\nFrom xlsx to csv.\n\n    $ xlparser source.xlsx new.csv \n\nFrom csv to xlsx.\n\n    $ xlparser source.csv new.xlsx \n\nFrom csv to json.\n\n    $ xlparser source.csv new.json\n\nFrom xlsx to csv(stdout).\n\n    $ xlparser source.xlsx | head \n\n    $ xlparser src.xlsx | tee test.csv\n    name, score\n    "李雷,韩梅",15\n    小花,16\n\nUse xcut to filter fields.\n\n    $ xlparser src.xlsx | xcut --from-csv -f name \n    name\n    "李雷,韩梅"\n    小花\n\n    $ xlparser src.xlsx | xcut --from-csv -f score,name\n    score,name\n    15,"李雷,韩梅"\n    16,小花\n\nConvert xlsx to csv\n\n    $ xlparser src.xlsx test.csv; \n    $ cat test.csv\n    name, age\n    李雷,15\n    小花,16\n\nConvert csv to json\n\n    $ xlparser test.csv test.json\n    [["name", "age"], ["李雷", "15"], ["小花", "16"]]\n\n### Module Usage\n\n#### Parse any type of file\n`parse` any type of file to rows:\n\n    >>> from xlparser import parse, saveCsv\n    >>> rows = parse(\'some.xlsx\')\n    >>> list(rows)\n    [[\'foo\', \'bar\'], [\'看\', \'我\', \'变\']]\n\nThe `parse` function supports the following file formats: .csv, .xls, .xlsx .\n\n#### Save to any type of file\nSave rows to csv\n\n    >>> from xlparser import saveCsv\n    >>> rows = [[\'foo\', \'bar\'], [\'看\', \'我\', \'变\']]\n    >>> saveCsv(rows, \'test.csv\')\n\nSave rows to xlsx\n\n    >>> saveXlsx(rows, \'test.xlsx\')\n\n#### Csv operation\n\n    >>> from xlparser import *\n\n    >>> rows = [(\'foo\',\'bar\'), (\'看\',\'我\',\'变\')]\n    >>> saveCsv(rows, \'test.csv\')\n\n    >>> list(parseCsv(\'test.csv\'))\n    [[\'foo\', \'bar\'], [\'看\', \'我\', \'变\']]\n\n#### Zip operation\n\n    >>> from xlparser import loadZip\n    >>> zf = loadZip(\'test.xlsx\')\n    >>> print(zf.filelist)\n    ......\n    >>> zf.extract(\'xl/media/image1.png\', \'/tmp\')\n    >>> os.rename(\'/tmp/\'+\'xl/media/image1.png\', \'./image1.png\')\n\n## Required\n1. python>=3.5\n2. xlrd: required by xls\n2. openpyxl>=2.5.4: required by xlsx\n',
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
