# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pokerlib', 'pokerlib.statistics']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pokerlib',
    'version': '0.6.0',
    'description': 'Python poker library',
    'long_description': " # pokerlib\n[![PyPI version](https://badge.fury.io/py/pokerlib.svg)](https://pypi.org/project/pokerlib)\n\n## General\nA Python poker library which focuses on simplifying a poker game implementation,\nwhen its io is supplied. It includes modules that help with hand parsing and poker game continuation.\n\nOne application of this library was made by the PokerMessenger app, \nwhich supplies library with io in the form of messenger group threads.\nThe app's repo is at https://github.com/kuco23/pokermessenger.\n\n## Tests\nBasic tests for this library are included. \nFor instance `round_test.py` can be started from os terminal, by typing `python round_test.py <player_num> <game_type>`,  after which a simulation is run with not-that-informative  data getting printed in stdout.\n\n## License\nGNU General Public License v3.0",
    'author': 'kuco23',
    'author_email': 'nseverkar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
