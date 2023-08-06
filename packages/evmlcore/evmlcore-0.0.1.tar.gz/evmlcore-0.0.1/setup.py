# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evmlcore']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'evmlcore',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'bishwarup.b',
    'author_email': 'bishwarup.b@eagleview.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
