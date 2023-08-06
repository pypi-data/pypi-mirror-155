# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nomadenv', 'nomadenv.resources']

package_data = \
{'': ['*']}

install_requires = \
['patchelf>=0.14.5,<0.15.0']

entry_points = \
{'console_scripts': ['nomadenv = nomadenv.__main__:main']}

setup_kwargs = {
    'name': 'nomadenv',
    'version': '0.1.5',
    'description': 'Build Movable Python Environments',
    'long_description': '# Nomadenv\n\n\n## Introduction\n\nNomadenv is a tool which help to build a python environnement which is easily delocalisable.',
    'author': 'Michael Delaporte',
    'author_email': 'michael@pixelscoder.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
