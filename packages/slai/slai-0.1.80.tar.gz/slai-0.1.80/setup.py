# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slai', 'slai.clients', 'slai.modules']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.26.0,<3.0.0',
 'urllib3>=1.26.7,<2.0.0']

setup_kwargs = {
    'name': 'slai',
    'version': '0.1.80',
    'description': '',
    'long_description': None,
    'author': 'slai',
    'author_email': 'luke@slai.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
