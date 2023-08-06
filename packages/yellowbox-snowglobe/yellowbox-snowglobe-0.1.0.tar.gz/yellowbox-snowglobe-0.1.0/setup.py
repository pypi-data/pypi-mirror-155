# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yellowbox_snowglobe']

package_data = \
{'': ['*']}

install_requires = \
['yellowbox[webserver,postgresql]>=0.7.0']

setup_kwargs = {
    'name': 'yellowbox-snowglobe',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Biocatch LTD',
    'author_email': 'serverteam@biocatch.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
