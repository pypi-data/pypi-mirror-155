# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuzzpyxl', 'fuzzpyxl.cell_compare', 'fuzzpyxl.utils']

package_data = \
{'': ['*']}

install_requires = \
['colormath>=3.0.0,<4.0.0', 'openpyxl>=3.0,<4.0']

entry_points = \
{'console_scripts': ['lint = ci.scripts:lint',
                     'lint_badge = ci.scripts:lint_badge',
                     'test = ci.scripts:test',
                     'test_report = ci.scripts:test_report',
                     'typecheck = ci.scripts:typecheck',
                     'typecheck_badge = ci.scripts:typecheck_badge']}

setup_kwargs = {
    'name': 'fuzzpyxl',
    'version': '0.0.4',
    'description': 'Helper functions to easily search for Excel-Cells by value, color, formatting or else',
    'long_description': None,
    'author': 'Jonas Hablitzel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JonasHablitzel/fuzzpyxl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
