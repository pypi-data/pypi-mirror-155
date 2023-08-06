# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytcm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytcm',
    'version': '0.3.1',
    'description': 'pytcm - Python Terminal Commands Manager',
    'long_description': '# pytcm\n\nA Python Terminal Commands Manager\n\n## Installation\n\n```\n$ pip install pytcm\n```\n\n## Usage\n\n### Using execute directly\n\n``` python\nimport pytcm\n\nbinary = \'python\'\nopts = [\n    pytcm.Flag(\'--version\', True)\n]\n\nresult = pytcm.execute(binary, opts)\n\nprint(result.out)  # "Python 3.9.7"\nprint(result.err)  # ""\nprint(result.returncode)  # 0\n```\n\n### Using a Command object that holds the context\n\n``` python\nimport pytcm\n\nbinary = \'python\'\nopts = [\n    pytcm.Flag(\'--version\', True)\n]\n\ncmd = pytcm.Command(binary, opts)\ncmd.execute()\n\nprint(cmd.out)  # "Python 3.9.7"\nprint(cmd.err)  # ""\nprint(cmd.returncode)  # 0\n```\n\n## Contributing\n\nThank you for considering making pytcm better.\n\nPlease refer to [docs](docs/CONTRIBUTING.md).\n\n## Change Log\n\nSee [CHANGELOG](CHANGELOG.md)\n\n## License\n\nMIT',
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
