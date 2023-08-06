# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stressed_cyrillic_tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stressed-cyrillic-tools',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Vuizur',
    'author_email': 'Vuizur@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
