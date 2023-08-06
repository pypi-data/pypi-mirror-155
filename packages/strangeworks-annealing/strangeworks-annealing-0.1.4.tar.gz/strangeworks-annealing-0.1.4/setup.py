# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strangeworks', 'strangeworks.annealing']

package_data = \
{'': ['*']}

install_requires = \
['dwave-embedding-utilities>=0.3.0,<0.4.0',
 'minorminer>=0.2.7,<0.3.0',
 'networkx>=2.6.3,<3.0.0',
 'strangeworks>=0.2.6,<0.3.0']

setup_kwargs = {
    'name': 'strangeworks-annealing',
    'version': '0.1.4',
    'description': 'Strangeworks Annealing SDK extension',
    'long_description': '| ⚠️    | This SDK is currently in pre-release alpha state and subject to change. To get more info or access to test features check out the [Strangeworks Backstage Pass Program](https://strangeworks.com/backstage). |\n|---------------|:------------------------|\n# Strangeworks Annealing Extension\n\n Strangeworks Python SDK extension for solving Annealing problems.\n\n\n \n For more information on using the SDK check out the [Strangeworks documentation](https://docs.strangeworks.com/).\n',
    'author': 'Strange Devs',
    'author_email': 'hello@strangeworks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
