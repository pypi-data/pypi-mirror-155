# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyattck', 'pyattck.utils']

package_data = \
{'': ['*'], 'pyattck': ['data/*']}

install_requires = \
['attrs>=21.4.0,<22.0.0',
 'fire>=0.4.0,<0.5.0',
 'pyattck-data>=2.3.0,<3.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pyattck',
    'version': '6.1.0',
    'description': 'A Python package to interact with the Mitre ATT&CK Frameworks',
    'long_description': None,
    'author': 'Swimlane',
    'author_email': 'info@swimlane.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
