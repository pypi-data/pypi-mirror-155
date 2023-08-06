# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['environment_variables', 'environment_variables.read']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'environment-variables-python',
    'version': '0.0.1',
    'description': 'this is not a awesome description',
    'long_description': '# python-environment',
    'author': 'Jorge Vasconcelos',
    'author_email': 'john@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jorgepvasconcelos/environment-variables-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
