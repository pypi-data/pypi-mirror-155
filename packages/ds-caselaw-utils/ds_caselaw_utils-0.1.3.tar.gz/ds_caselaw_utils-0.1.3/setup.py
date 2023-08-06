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
    'version': '0.1.3',
    'description': 'Utilities for the National Archives Caselaw project',
    'long_description': '# Caselaw utility functions\n\npypi name: [ds-caselaw-utils](https://pypi.org/project/ds-caselaw-utils)\npython import name: `ds_caselaw_utils`\n\nThis repo contains functions of general use throughout the National Archives Caselaw project\nso that we can have a single point of truth potentially across many repositories.\n\n## Examples\n\n```\nfrom ds_caselaw_utils import neutral_url\nneutral_url("[2022] EAT 1")  # \'/eat/2022/4\'\n```\n',
    'author': 'David McKee',
    'author_email': 'dragon@dxw.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nationalarchives/ds-caselaw-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
