# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fucker_110']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'fucker-110',
    'version': '2.0.0',
    'description': '',
    'long_description': None,
    'author': '蒋经伟',
    'author_email': 'jingwei.jiang@mihoyo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
