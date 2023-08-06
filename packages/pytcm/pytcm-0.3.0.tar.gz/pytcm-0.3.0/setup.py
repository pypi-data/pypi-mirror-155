# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytcm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytcm',
    'version': '0.3.0',
    'description': 'pytcm - Python Terminal Commands Manager',
    'long_description': '# pytcm\n\nA Python Terminal Commands Manager',
    'author': 'Alexis Beaulieu',
    'author_email': 'alexisbeaulieu97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alexisbeaulieu97/pytcm',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
