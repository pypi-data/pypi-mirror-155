# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uc_browser_scrapy']

package_data = \
{'': ['*']}

install_requires = \
['Scrapy>=2.6.1,<3.0.0', 'uc-browser>=0.2.4,<0.3.0']

setup_kwargs = {
    'name': 'uc-browser-scrapy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Thiago Oliveira',
    'author_email': 'thiceconelo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
