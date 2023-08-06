# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thehouse', 'thehouse.characters', 'thehouse.helpers', 'thehouse.rooms']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['thehouse = thehouse.play:play']}

setup_kwargs = {
    'name': 'thehouse',
    'version': '1.2.1',
    'description': 'A text-based game written in python',
    'long_description': '# the house\n\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\nA text-based game written in python\n\n## Install or Download\n\nYou can install the game with pip by typing `pip install thehouse`\n\nor you can download this repository and\n\n## Play\n\nIf you have installed **thehouse** via pip you can call the game and run it by typing `thehouse`.\n\nIf you downloaded the repository, on the root of the repo run `python thehouse` and the game will start!\n',
    'author': 'Davide Di Criscito',
    'author_email': 'davide.dicriscito@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ctrlmaniac/the-house/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
