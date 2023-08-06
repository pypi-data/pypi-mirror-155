# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonfeed2social', 'jsonfeed2social.social']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'configparser>=5.2.0,<6.0.0',
 'requests>=2.28.0,<3.0.0',
 'tweepy>=4.10.0,<5.0.0']

setup_kwargs = {
    'name': 'jsonfeed2social',
    'version': '1.0.1',
    'description': 'Tweet and toot from your jsonfeeed',
    'long_description': None,
    'author': 'Fundor333',
    'author_email': 'fundor333@fundor333.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
