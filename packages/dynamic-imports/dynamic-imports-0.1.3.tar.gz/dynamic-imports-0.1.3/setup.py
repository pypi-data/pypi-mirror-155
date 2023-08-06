# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamic_imports']

package_data = \
{'': ['*']}

install_requires = \
['ready-logger>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'dynamic-imports',
    'version': '0.1.3',
    'description': 'Dynamic discovery and importing.',
    'long_description': None,
    'author': 'Dan Kelleher',
    'author_email': 'dan@danklabs.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
