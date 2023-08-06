# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['az_evgrid_pydantic_schema']

package_data = \
{'': ['*']}

install_requires = \
['datamodel-code-generator>=0.13.0,<0.14.0', 'pydantic>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'az-evgrid-pydantic-schema',
    'version': '0.1.0',
    'description': 'Azure Event Grid の event schema  を Pydantic Model で提供',
    'long_description': '使い方は [GitHubRepository](https://github.com/nnashiki/az-evgrid-pydantic-schema) をご参照ください。\n',
    'author': 'Niten Nashiki',
    'author_email': 'n.nashiki.work@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nnashiki/az-evgrid-pydantic-schema',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
