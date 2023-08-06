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
    'version': '0.2.0',
    'description': 'CLI application for managing servers on the Hetzner platform',
    'long_description': '# hetzner-control\nCLI application for managing servers on [the Hetzner platform](https://www.hetzner.com/)\n\n',
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
