# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ds_caselaw_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ds-caselaw-utils',
    'version': '0.1.2',
    'description': 'Utilities for the National Archives Caselaw project',
    'long_description': None,
    'author': 'David McKee',
    'author_email': 'dragon@dxw.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
