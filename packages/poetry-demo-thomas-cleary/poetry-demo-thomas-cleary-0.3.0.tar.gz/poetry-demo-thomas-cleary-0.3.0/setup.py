# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo_thomas_cleary']

package_data = \
{'': ['*'], 'poetry_demo_thomas_cleary': ['data/*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['poetry-demo-thomas-cleary = '
                     'poetry_demo_thomas_cleary.cli:run']}

setup_kwargs = {
    'name': 'poetry-demo-thomas-cleary',
    'version': '0.3.0',
    'description': 'Example of setting up a python package project with poetry',
    'long_description': '# Poetry Demo Thomas Cleary\nAn example of setting up a package with poetry',
    'author': 'Thomas Cleary',
    'author_email': 'thomasclearydev@gmail.com',
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
