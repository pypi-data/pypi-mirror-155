# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hetzner_control', 'hetzner_control.commands', 'hetzner_control.core']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'rich>=12.0.0,<13.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['htz = hetzner_control.cli:main']}

setup_kwargs = {
    'name': 'hetzner-control',
    'version': '0.3.0',
    'description': 'CLI application for managing servers on the Hetzner platform',
    'long_description': '# hetzner-control\n\n\n`hetzner-control` its CLI tool, which lets you easily manage servers on [the Hetzner platform](https://www.hetzner.com/)\n\n![Sample usage gif](./assets/sample_usage.gif)\n\n## Table of contents\n* [Motivation](#Motivation)\n* [Usage](#Usage)\n* [Installation guide](#Installation-guide)\n* [Want to contribute?](#Want-to-contribute?)\n* [License](#License)\n\n## Motivation\n\nI wanted to create a console application that would interact \nwith the REST API of the cloud service for convenient server management\nand the platform in general. \n\nI also wanted to improve my skills in application\ndesign and API work while I\'m studying software engineering in university.\n\n## Usage\n\n```shell\n$ htz [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show documentation message for available commands/flags\n\n**Commands**:\n\n* `info`: Information about available data centers, servers, prices\n* `server`: Operations with servers\n* `version`: Show app version\n\n[For a more detailed description of the command, see wiki page](https://github.com/Hanabiraa/hetzner-control/wiki)\n\n## Installation guide\n1. First, install environment variable, i.e. in .bashrc\n```shell\n$ export HETZNER_API_TOKEN="YOUR_HETZNER_TOKEN_HERE"\n```\n\n2. Installation option\n   * You can install hetzner-control from pip \n      ```shell\n      $ pip3 install hetzner-control\n      ```\n   * Or you can clone the repository and build the wheel/sdist module with poetry (you can preinstall poetry):\n       ```shell\n       $ git clone https://github.com/Hanabiraa/hetzner-control.git\n       $ cd hetzner-control\n       $ poetry install\n       $ poetry build\n       ```\n\n## Want to contribute?\n\n1. Clone repo and create a new branch: $ git checkout https://github.com/Hanabiraa/hetzner-control -b name_for_new_branch.\n2. Make changes and test\n3. Submit Pull Request with comprehensive description of changes\n\n## License\n\nMIT License',
    'author': 'Hanabira',
    'author_email': 'workflow.elec@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
