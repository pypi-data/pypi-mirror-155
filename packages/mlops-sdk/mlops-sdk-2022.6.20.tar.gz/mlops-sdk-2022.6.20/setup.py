# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlops_sdk',
 'mlops_sdk.config',
 'mlops_sdk.experiments',
 'mlops_sdk.ml',
 'mlops_sdk.models',
 'mlops_sdk.utils']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.9b0,<22.0',
 'boto3>=1.24.12,<2.0.0',
 'flake8>=4.0.1,<5.0.0',
 'hvac>=0.11.2,<0.12.0',
 'pyfiglet>=0.8.post1,<0.9',
 'requests>=2.26.0,<3.0.0',
 'slack-sdk>=3.11.2,<4.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'termcolor>=1.1.0,<2.0.0']

extras_require = \
{'all': ['torch>=1.10.0,<2.0.0',
         'torchdiffeq>=0.2.2,<0.3.0',
         'tensorboard>=2.7.0,<3.0.0'],
 'models-torch': ['torch>=1.10.0,<2.0.0',
                  'torchdiffeq>=0.2.2,<0.3.0',
                  'tensorboard>=2.7.0,<3.0.0']}

setup_kwargs = {
    'name': 'mlops-sdk',
    'version': '2022.6.20',
    'description': 'mlops-sdk for data play',
    'long_description': None,
    'author': 'AI Engineering Chapter 정유선',
    'author_email': 'jerryjung@emart.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.8,<=3.9.5',
}


setup(**setup_kwargs)
