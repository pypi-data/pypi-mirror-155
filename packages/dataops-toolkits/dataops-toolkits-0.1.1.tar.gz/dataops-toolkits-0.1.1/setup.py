# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataops_toolkits', 'dataops_toolkits.scripts']

package_data = \
{'': ['*']}

install_requires = \
['label-studio==1.5.0']

entry_points = \
{'console_scripts': ['jsonconvert = dataops_toolkits.scripts.jsonconvert:main']}

setup_kwargs = {
    'name': 'dataops-toolkits',
    'version': '0.1.1',
    'description': 'Gadget Collection of DataOps in MLOps',
    'long_description': '# dataops\nGadget Collection of DataOps in MLOps\n',
    'author': 'yuiant',
    'author_email': 'gyuiant@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yuiant/dataops',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
