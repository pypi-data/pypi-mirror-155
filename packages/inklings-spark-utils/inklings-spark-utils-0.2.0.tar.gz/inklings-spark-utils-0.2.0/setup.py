# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inklings_spark_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'inklings-spark-utils',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Adrian Abreu',
    'author_email': 'adrianabreugonzalez@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
