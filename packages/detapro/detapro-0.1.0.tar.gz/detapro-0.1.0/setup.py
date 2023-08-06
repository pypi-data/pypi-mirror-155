# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['detapro']

package_data = \
{'': ['*']}

install_requires = \
['deta>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'detapro',
    'version': '0.1.0',
    'description': 'A python package that further empowers the orginal Detabase ',
    'long_description': None,
    'author': 'TheReaper62',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
