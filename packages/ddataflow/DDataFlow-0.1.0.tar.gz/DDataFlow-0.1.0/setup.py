# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ddataflow', 'ddataflow.samples']

package_data = \
{'': ['*']}

install_requires = \
['databricks-cli>=0.16.6,<0.17.0', 'pyspark>=3.2.1,<4.0.0']

entry_points = \
{'console_scripts': ['mltools = ddataflow_cli']}

setup_kwargs = {
    'name': 'ddataflow',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
