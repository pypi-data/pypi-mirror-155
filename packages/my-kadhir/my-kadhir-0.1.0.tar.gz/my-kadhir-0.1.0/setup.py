# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_kadhir']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'my-kadhir',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'kadhiresh',
    'author_email': 'kgajindren@project44.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
