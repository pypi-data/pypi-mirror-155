# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['k3sconfig']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.4,<9.0.0',
 'fastapi>=0.75.1,<0.76.0',
 'requests>=2.27.1,<3.0.0',
 'uvicorn[standard]>=0.17.6,<0.18.0']

entry_points = \
{'console_scripts': ['k3sconfig = k3sconfig.app:cli']}

setup_kwargs = {
    'name': 'k3sconfig',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Anatoly Gusev',
    'author_email': 'gusev.tolia@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
