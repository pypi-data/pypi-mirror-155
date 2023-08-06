# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo_thomas_cleary']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'poetry-demo-thomas-cleary',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Thomas Cleary',
    'author_email': 'thomasclearydev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
