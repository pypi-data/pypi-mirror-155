# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmem_plugin_graphql']

package_data = \
{'': ['*']}

install_requires = \
['cmem-plugin-base>=1.2.0',
 'gql[all]>=3.2.0,<4.0.0',
 'validators>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'cmem-plugin-graphql',
    'version': '1.0.0a1',
    'description': 'eccenca Corporate Memory workflow plugin that executes a custom GraphQL query to a GraphQL endpoint and saves the result to a JSON dataset.',
    'long_description': '# cmem-plugin-graphql\n\na CMEM Plugin to query GraphQL APIs and write the response to dataset of type JSON.\nIn the current release we are supporting only endpoints without authentication.\n',
    'author': 'Sai Praneeth M',
    'author_email': 'saipraneeth@aarth.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
