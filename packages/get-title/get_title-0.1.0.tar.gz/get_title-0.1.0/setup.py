# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['get_title']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0', 'requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'get-title',
    'version': '0.1.0',
    'description': 'get the title of a web page',
    'long_description': None,
    'author': 'albert patterson',
    'author_email': 'apatterson189@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
