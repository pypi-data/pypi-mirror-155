# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aimol']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['posgen = aimol:main']}

setup_kwargs = {
    'name': 'aimol',
    'version': '0.0.0.1',
    'description': 'AIMol',
    'long_description': None,
    'author': 'Rahul Brahma',
    'author_email': 'mrbrahma.rahul@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/takshan/posgen',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
