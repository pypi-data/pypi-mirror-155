# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forgeheroku']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.0,<9.0.0',
 'forge-core<1.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0']

entry_points = \
{'console_scripts': ['forge-heroku = forgeheroku:cli']}

setup_kwargs = {
    'name': 'forge-heroku',
    'version': '0.1.0',
    'description': 'Work library for Forge',
    'long_description': '# forge-heroku\n',
    'author': 'Dave Gaeddert',
    'author_email': 'dave.gaeddert@dropseed.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.forgepackages.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
