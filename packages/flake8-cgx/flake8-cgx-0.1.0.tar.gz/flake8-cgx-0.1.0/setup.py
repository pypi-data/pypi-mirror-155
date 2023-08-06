# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_cgx']

package_data = \
{'': ['*']}

install_requires = \
['collagraph>=0.4.1', 'flake8>=4.0.0']

entry_points = \
{'flake8.extension': ['CGX = flake8_cgx:CGXTreeChecker']}

setup_kwargs = {
    'name': 'flake8-cgx',
    'version': '0.1.0',
    'description': 'Flake8 plugin for cgx (Collagraph single file component) files',
    'long_description': '# flake8-cgx\n\nFlake8 plugin for linting of cgx files (Single File Components for [Collagraph](https://github.com/fork-tongue/collagraph)).\n',
    'author': 'Berend Klein Haneveld',
    'author_email': 'berendkleinhaneveld@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
