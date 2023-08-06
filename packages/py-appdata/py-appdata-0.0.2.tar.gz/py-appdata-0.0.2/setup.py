# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['appdata']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-appdata',
    'version': '0.0.2',
    'description': 'Small utility library to provide easy access to files and key-value store in an application directory',
    'long_description': '# Python App Data\nThe py-appdata aims to solve the issue of storing simple application data and accessing it in an easy way.\n\nThe core idea is to expose a simple interface that has two properties\n - A get/set interface to simple values\n - A simple way of saving and retrieving files from the application directory\n\n## Stores\nThe `AppData` class provides an interface to two storage-abstractions: A file system and a key-value store. This lets\nyou easily save/retrieve files as well as setting/loading key/values which is a common app-data usage.\n\n## Get started\n````python\nfrom appdata import appdata\nfrom datetime import datetime, timezone\n\n# defaults to app_data\nappdata.set_file_store("my_app_data_dir")\n\n# defaults to kv_store\nappdata.set_key_value_store("my_store")\n\nappdata["last_login"] = datetime.utcnow().replace(tzinfo=timezone.utc)\n\nwith appdata.write("some_file.txt") as f:\n    f.write("Mjello")\n````\n\n## Dataclass support\nIf you like type hints, you can register a `dataclass` instance as a proxy for the key-value store\n```python\nfrom appdata import appdata\nfrom datetime import datetime, timezone\nfrom dataclasses import dataclass\n\n\n# Define the dataclass\n@dataclass\nclass KV:\n    last_login: datetime = None\n\n\n# Create an object to be referenced and register it to appdata\nkv = KV()\nappdata.register(kv)\n\n\n# The KeyValue object now acts as a proxy, and can be used throughout your project\nkv.last_login = datetime.utcnow().replace(tzinfo=timezone.utc)\n```',
    'author': 'Jesper Jensen',
    'author_email': 'mail@jeshj.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gedemagt/appdata',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
