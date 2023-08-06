# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kolorz']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['kolorz = kolorz.cli:kolor']}

setup_kwargs = {
    'name': 'kolorz',
    'version': '0.1.0',
    'description': 'A fast, extensible, and kolorful python library to print colored output to the terminal',
    'long_description': '<h2 align="center"> ━━━━━━  ❖  ━━━━━━ </h2>\n\n<!-- BADGES -->\n<div align="center">\n   <p></p>\n   \n   <img src="https://img.shields.io/github/stars/dotzenith/kolorz?color=F8BD96&labelColor=302D41&style=for-the-badge">   \n\n   <img src="https://img.shields.io/github/forks/dotzenith/kolorz?color=DDB6F2&labelColor=302D41&style=for-the-badge">   \n\n   <img src="https://img.shields.io/github/repo-size/dotzenith/kolorz?color=ABE9B3&labelColor=302D41&style=for-the-badge">\n   \n   <img src="https://badges.pufler.dev/visits/dotzenith/kolorz?style=for-the-badge&color=96CDFB&logoColor=white&labelColor=302D41"/>\n   <br>\n</div>\n\n<p/>\n\n---\n\n### ❖ Information \n\n  kolorz is a simple, fast, and extensible python library to facilitate printing colors to the terminals that support true color  \n\n  <img src=".assets/kolorz.gif" alt="kolorz gif">\n\n---\n\n### ❖ Installation\n\n> Install from pip\n```sh\npip3 install kolorz\n```\n\n> Install from source\n- First, install [poetry](https://python-poetry.org/)\n```sh\ngit clone https://github.com/dotzenith/kolorz.git\ncd kolorz\npoetry build\npip3 install ./dist/kolorz-0.1.0.tar.gz\n```\n\n### ❖ Usage \n\n- TODO\n\n---\n\n### ❖ About kolorz\n\n- TODO\n\n---\n\n### ❖ What\'s New? \n0.1.0 - Initial release\n\n---\n\n<div align="center">\n\n   <img src="https://img.shields.io/static/v1.svg?label=License&message=MIT&color=F5E0DC&labelColor=302D41&style=for-the-badge">\n\n</div>\n',
    'author': 'dotzenith',
    'author_email': 'contact@danshu.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
