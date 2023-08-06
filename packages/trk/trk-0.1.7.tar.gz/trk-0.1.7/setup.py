# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trk']

package_data = \
{'': ['*']}

install_requires = \
['archieml>=0.3.5,<0.4.0',
 'pandas>=1.4.1,<2.0.0',
 'plotext>=4.2.0,<5.0.0',
 'requests>=2.27.1,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['trk = trk.cli:app']}

setup_kwargs = {
    'name': 'trk',
    'version': '0.1.7',
    'description': '',
    'long_description': '# Trk: A CLI Time Tracker\n\nA handy cli time tracker',
    'author': 'nick',
    'author_email': 'nickmcmillanproductions@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
