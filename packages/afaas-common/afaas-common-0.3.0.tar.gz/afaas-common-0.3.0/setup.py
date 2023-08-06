# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['afaas',
 'afaas.cache',
 'afaas.common',
 'afaas.tests',
 'afaas.tests.cache',
 'afaas.tests.common']

package_data = \
{'': ['*'], 'afaas.tests.cache': ['data/*'], 'afaas.tests.common': ['data/*']}

install_requires = \
['biopython>=1.79,<2.0', 'google-cloud-firestore>=2.4.0,<3.0.0']

setup_kwargs = {
    'name': 'afaas-common',
    'version': '0.3.0',
    'description': 'Alphafold as a Service common packages',
    'long_description': None,
    'author': 'Cradle Bio',
    'author_email': 'cl@cradle.bio',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
