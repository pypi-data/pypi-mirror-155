# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataops_toolkits']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dataops-toolkits',
    'version': '0.1.0',
    'description': 'Gadget Collection of DataOps in MLOps',
    'long_description': None,
    'author': 'yuiant',
    'author_email': 'gyuiant@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
