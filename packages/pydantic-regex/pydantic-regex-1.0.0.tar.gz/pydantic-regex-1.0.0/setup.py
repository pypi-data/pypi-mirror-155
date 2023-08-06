# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_regex']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-regex',
    'version': '1.0.0',
    'description': 'Regular expression to pydantic model parser.',
    'long_description': None,
    'author': 'Oleksandr Hiliazov',
    'author_email': 'oleksandr.hiliazov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<3.11',
}


setup(**setup_kwargs)
