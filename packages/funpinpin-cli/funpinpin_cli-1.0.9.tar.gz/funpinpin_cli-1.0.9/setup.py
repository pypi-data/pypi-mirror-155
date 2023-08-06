# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['funpinpin_cli',
 'funpinpin_cli.core',
 'funpinpin_cli.core.populate',
 'funpinpin_cli.core.util',
 'funpinpin_cli.scripts',
 'funpinpin_cli.scripts.app',
 'funpinpin_cli.scripts.extension',
 'funpinpin_cli.scripts.populate',
 'funpinpin_cli.tests',
 'funpinpin_cli.tests.util']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'click>=8.1.2,<9.0.0',
 'haikunator>=2.1.0,<3.0.0',
 'pickleDB>=0.9.2,<0.10.0',
 'psutil>=5.9.1,<6.0.0',
 'python-graphql-client>=0.4.3,<0.5.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['funpinpin = funpinpin_cli.scripts.command:cli']}

setup_kwargs = {
    'name': 'funpinpin-cli',
    'version': '1.0.9',
    'description': 'funpinpin cli tool',
    'long_description': 'Funpinpin Cli\n\n```sh\nUse funpinpin -h to see avaliable commands.\n``` \n\n\n',
    'author': 'funpinpin',
    'author_email': 'support@funpinpin.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
