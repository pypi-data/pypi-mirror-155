# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jledru_maths']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jledru-maths',
    'version': '0.1.1',
    'description': 'Testing package deployment',
    'long_description': '# Testing poetry ',
    'author': 'Julien Ledru',
    'author_email': 'julien.ledru@hei.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jledru/jledru_maths/releases/tag/v0.1.1',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
