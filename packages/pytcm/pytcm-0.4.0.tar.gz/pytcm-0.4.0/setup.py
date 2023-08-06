# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytcm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytcm',
    'version': '0.4.0',
    'description': 'pytcm - Python Terminal Commands Manager',
    'long_description': '# pytcm\n\nA Python Terminal Commands Manager\n\n## Installation\n\n```\n$ pip install pytcm\n```\n\n## Usage\n\n### Using execute directly\n\n``` python\nimport pytcm\n\nbinary = \'python\'\nopts = [\n    pytcm.Flag(\'--version\', True)\n]\n\nresult = pytcm.execute(binary, opts)\n\nprint(result.out)  # "Python 3.9.7"\nprint(result.err)  # ""\nprint(result.returncode)  # 0\n```\n\n### Using a Command object that holds the context\n\n``` python\nimport pytcm\n\nbinary = \'python\'\nopts = [\n    pytcm.Flag(\'--version\', True)\n]\n\ncmd = pytcm.Command(binary, opts)\ncmd.execute()\n\nprint(cmd.out)  # "Python 3.9.7"\nprint(cmd.err)  # ""\nprint(cmd.returncode)  # 0\n```\n\n## Options\n\n### Flag\n\nA boolean option\n\n```python\nimport pytcm\n\nflag = pytcm.Flag("--verbose", True)\nopt = flag.parse()\n\nprint(opt)  # "--verbose"\n```\n\n### Explicit\n\nAn option with an equal sign\n\n```python\nimport pytcm\n\nexplicit = pytcm.Explicit("--age", 12)\nopt = explicit.parse()\n\nprint(opt)  # "--age=12"\n```\n\n### Implicit\n\nAn option separated by a space character\n\n```python\nimport pytcm\n\nimplicit = pytcm.Implicit("--age", 12)\nopt = implicit.parse()\n\nprint(opt)  # "--age 12"\n```\n\n### Positional\n\nA simple inline option\n\n```python\nimport pytcm\n\npositional = pytcm.Positional("test.txt")\nopt = positional.parse()\n\nprint(opt)  # "test.txt"\n```\n\n## Contributing\n\nThank you for considering making pytcm better.\n\nPlease refer to [docs](docs/CONTRIBUTING.md).\n\n## Change Log\n\nSee [CHANGELOG](CHANGELOG.md)\n\n## License\n\nMIT',
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
