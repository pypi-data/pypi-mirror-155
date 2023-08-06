# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['topyn', 'topyn.commands']

package_data = \
{'': ['*'], 'topyn': ['configs/*']}

install_requires = \
['autoflake>=1.4.0,<1.5.0',
 'black>=22.0.0,<23.0.0',
 'click>=8.0.0,<9.0.0',
 'flake8-bugbear',
 'flake8-comprehensions',
 'flake8-print',
 'flake8>=4.0.0,<5.0.0',
 'mypy',
 'pep8-naming',
 'toml']

entry_points = \
{'console_scripts': ['topyn = topyn:console.run']}

setup_kwargs = {
    'name': 'topyn',
    'version': '0.7.0',
    'description': 'TOPyN: Typed Opinionated PYthon Normalizer',
    'long_description': '# TOPyN: Typed Opinionated PYthon Normalizer\n<p>\n    <a href="https://github.com/lleites/topyn/actions"><img alt="Actions Status" src="https://github.com/lleites/topyn/workflows/Test/badge.svg"></a>\n    <a href="https://github.com/lleites/topyn/actions"><img alt="Actions Status" src="https://github.com/lleites/topyn/workflows/Topyn/badge.svg"></a>\n    <a href="https://coveralls.io/github/lleites/topyn?branch=HEAD"><img alt="Coverage Status" src="https://coveralls.io/repos/github/lleites/topyn/badge.svg?branch=HEAD"></a>\n    <a href="https://github.com/lleites/topyn/blob/master/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>\n    <a href="https://pypi.org/project/topyn/"><img alt="PyPI" src="https://img.shields.io/pypi/v/topyn"></a>\n</p>\n\n## About\n<p align="center">\n    <img src="https://github.com/lleites/topyn/blob/master/scooter.svg" alt="Scooter" width="300"/>*\n</p>\nPython is quite a flexible language, something that is not so good if you start working in mid level size projects and/or in teams.\nOver the time we have found a set of rules that makes working with Python in this context easier, and once you get you use to them you want to apply them to every small Python snippet that you write.\n\nThe problem is that these rules depend on a set of packages and config files, and every time we change our mind about one rule, or add new ones, we need to update multiple projects.\nTopyn solves this by providing in one single place all the tools and configurations we use in our projects.\n\nAll the configurations are part of the project (`topyn/configs`) and is not the purpose of this project to make them flexible, if you need that please check the packages that we use, and run them with your configuration.\n\n## Install\n`pip install topyn`\n\n## Command line\nThere are two possible arguments:\n* `path` is the path that you want to check, if it is empty it defaults to the current directory.\n* `--fix` if you use this flag topyn will try to fix the code for you\n\n### Examples\nCheck the code inside directory_with_code : `topyn directory_with_code`\n\nCheck the code inside current directory : `topyn`\n\nCheck the code inside current directory and try to fix it: `topyn --fix`\n\n### `topyn --help` output\n\n```\nTyped Opinionated PYthon Normalizer\n\npositional arguments:\n  path        path to topynize (default: .)\n\noptional arguments:\n  -h, --help  show this help message and exit\n  --fix       try to fix my code (default: False)\n  --version   show program\'s version number and exit\n```\n\n### `topyn` output\n✅\n```\n➡️ Checking formatting ...\nAll done! ✨ 🍰 ✨\n8 files would be left unchanged.\n➡️ Checking rules ...\n➡️ Checking types ...\n✅ Everything is OK! 😎"\n```\n🔴 \n```\n➡️ Checking formatting ...\nAll done! ✨ 🍰 ✨\n1 file would be left unchanged.\n➡️ Checking rules ...\n➡️ Checking types ...\ntests/resources/wrong_types/wrong_types.py:2: error: Incompatible return value type (got "int", expected "str")\nFound 1 error in 1 file (checked 1 source file)\n\n🔴 Sadly, types failed 😢\n```\n\n\n## Tools included\n\n### [Flake8](https://github.com/PyCQA/flake8)\nflake8 is a command-line utility for enforcing style consistency across Python projects\n\n#### Flake8 plugins\n* #### [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear)\n  A plugin for flake8 finding likely bugs and design problems in your program. Contains warnings that don\'t belong in pyflakes and pycodestyle. \n* #### [flake8-print](https://github.com/JBKahn/flake8-print)\n  Check for `print` statements in python files.\n* #### [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions)\n  A flake8 plugin that helps you write better list/set/dict comprehensions.\n* #### [pep8-naming](https://github.com/PyCQA/pep8-naming)\n  Naming Convention checker for Python (PEP 8)\n### [Black](https://github.com/psf/black)\nThe Uncompromising Code Formatter\n### [Mypy](https://github.com/python/mypy)\nOptional static typing for Python (PEP 484) \n\n## Contributors\nLeandro Leites Barrios : Main developer\n\nDenada Korita : UX & Documentation consultant \n\n---\n\\* scooter icon source: [icons8](https://icons8.com/)\n',
    'author': 'Leandro Leites Barrios',
    'author_email': 'laloleites@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lleites/topyn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
