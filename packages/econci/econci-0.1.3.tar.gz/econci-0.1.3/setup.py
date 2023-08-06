# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['econci']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.4', 'pandas>=0.25.0']

setup_kwargs = {
    'name': 'econci',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'phcsoares',
    'author_email': 'phcastrosoares@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
