# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['appdata']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-appdata',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Jesper Jensen',
    'author_email': 'mail@jeshj.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
