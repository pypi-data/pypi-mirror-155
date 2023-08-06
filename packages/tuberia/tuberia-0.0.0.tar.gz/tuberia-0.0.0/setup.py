# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tuberia']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'prefect>=1.2.0,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'typer>=0.4.0,<0.5.0']

extras_require = \
{'pyspark': ['pyspark==3.2.0', 'delta-spark==1.1.0']}

entry_points = \
{'console_scripts': ['tuberia = tuberia.__main__:main']}

setup_kwargs = {
    'name': 'tuberia',
    'version': '0.0.0',
    'description': 'Tuberia... when data engineering meets software engineering',
    'long_description': '\n                          ▄▄▄█████▓ █    ██  ▄▄▄▄   ▓█████  ██▀███   ██▓ ▄▄▄\n                          ▓  ██▒ ▓▒ ██  ▓██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒▓██▒▒████▄\n                          ▒ ▓██░ ▒░▓██  ▒██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒▒██▒▒██  ▀█▄\n                          ░ ▓██▓ ░ ▓▓█  ░██░▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄  ░██░░██▄▄▄▄██\n                            ▒██▒ ░ ▒▒█████▓ ░▓█  ▀█▓░▒████▒░██▓ ▒██▒░██░ ▓█   ▓██▒\n                            ▒ ░░   ░▒▓▒ ▒ ▒ ░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░░▓   ▒▒   ▓▒█░\n                              ░    ░░▒░ ░ ░ ▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░ ▒ ░  ▒   ▒▒ ░\n                            ░       ░░░ ░ ░  ░    ░    ░     ░░   ░  ▒ ░  ░   ▒\n                                      ░      ░         ░  ░   ░      ░        ░  ░\n\n<p align="center">\n    <img src="https://github.com/aidictive/tuberia/actions/workflows/cicd.yaml/badge.svg" alt="Tuberia CI pipeline status">\n    <img src="https://img.shields.io/codecov/c/github/aidictive/tuberia" alt="Tuberia coverage status">\n    <img src="https://img.shields.io/github/contributors/aidictive/tuberia" alt="Tuberia contributors">\n    <img src="https://pepy.tech/badge/tuberia" alt="Tuberia total downloads">\n    <img src="https://pepy.tech/badge/tuberia/month" alt="Tuberia downloads per month">\n    <br />\n    Data engineering meets software engineering.\n</p>\n<hr>\n\n\n## Getting started\n\nYou need:\n\n* Spark 3.2.\n* Java JDK 11 (Required by Spark).\n* [Poetry](https://python-poetry.org/docs/#installation).\n* Make.\n\nOnce you have all the tools installed just open a shell on the root folder of\nthe project and install the dependencies in a new virtual environment with:\n\n```sh\n$ make install\n```\n\nThe previous command also installs some [pre-commits](https://pre-commit.com).\n\nCheck that your package is installed with:\n\n```sh\n$ poetry run tuberia\n▄▄▄█████▓ █    ██  ▄▄▄▄   ▓█████  ██▀███   ██▓ ▄▄▄\n▓  ██▒ ▓▒ ██  ▓██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒▓██▒▒████▄\n▒ ▓██░ ▒░▓██  ▒██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒▒██▒▒██  ▀█▄\n░ ▓██▓ ░ ▓▓█  ░██░▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄  ░██░░██▄▄▄▄██\n  ▒██▒ ░ ▒▒█████▓ ░▓█  ▀█▓░▒████▒░██▓ ▒██▒░██░ ▓█   ▓██▒\n  ▒ ░░   ░▒▓▒ ▒ ▒ ░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░░▓   ▒▒   ▓▒█░\n    ░    ░░▒░ ░ ░ ▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░ ▒ ░  ▒   ▒▒ ░\n  ░       ░░░ ░ ░  ░    ░    ░     ░░   ░  ▒ ░  ░   ▒\n            ░      ░         ░  ░   ░      ░        ░  ░\nVersion 0.0.0\n```\n\nIf you can see that funky logo your installation is correct. Note that the\nversion may change.\n\nIf you do not want to use `poetry run` in front of all your commands just\nactivate the virtual environment with `poetry shell`. Use `exit` if you want to\ndeactivate the environment.\n\n\n## How do I build the package?\n\nYou can build the package without installing the dependencies or without a\nproper Spark installation. Use `make build` or just `make`. You should see\nsomething like:\n\n```sh\n$ make\npoetry build\nBuilding tuberia (0.0.0)\n  - Building sdist\n  - Built tuberia-0.0.0.tar.gz\n  - Building wheel\n  - Built tuberia-0.0.0-py3-none-any.whl\n```\n\n\n## How do I run tests?\n\nRun tests locally with:\n\n```sh\n$ make test\n```\n\n\n## Contribution guidelines\n\n* The code is auto-formatted by Black, so you can write the code without\nfollowing any style guide and Black will take care of making it consistent\nwith the current codebase.\n* Write tests: test not added in the PR, test that will never be added.\n',
    'author': 'guiferviz',
    'author_email': 'guiferviz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aidictive/tuberia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
