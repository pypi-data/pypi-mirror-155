# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rm2trash', 'rm2trash.commands', 'rm2trash.core']

package_data = \
{'': ['*']}

install_requires = \
['termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['rm2trash = rm2trash.commands.rm2trash:main']}

setup_kwargs = {
    'name': 'rm2trash',
    'version': '0.1.1',
    'description': 'Simple trash commands.',
    'long_description': None,
    'author': 'Kuangye Chen',
    'author_email': 'chen.kuangye@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
