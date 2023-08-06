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
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Julien Ledru',
    'author_email': 'julien.ledru@hei.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
