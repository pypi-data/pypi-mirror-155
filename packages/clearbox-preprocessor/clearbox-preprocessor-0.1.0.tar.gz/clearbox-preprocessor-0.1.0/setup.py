# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clearbox_preprocessor', 'clearbox_preprocessor.transformers']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.4,<2.0.0', 'pandas>=1.4.2,<2.0.0', 'scikit-learn>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'clearbox-preprocessor',
    'version': '0.1.0',
    'description': 'A very basic implementation of a preprocessor for tabular data.',
    'long_description': '',
    'author': "Carmine D'Amico",
    'author_email': 'carmine@clearbox.ai',
    'maintainer': "Carmine D'Amico",
    'maintainer_email': 'carmine@clearbox.ai',
    'url': 'https://github.com/clearbox-ai/preprocessor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
