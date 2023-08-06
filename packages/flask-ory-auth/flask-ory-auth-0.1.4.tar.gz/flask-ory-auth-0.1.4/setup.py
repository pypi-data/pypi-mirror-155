# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_ory_auth',
 'flask_ory_auth.hydra',
 'flask_ory_auth.keto',
 'flask_ory_auth.kratos']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.2,<3.0.0',
 'requests-oauthlib>=1.3.1,<2.0.0',
 'requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'flask-ory-auth',
    'version': '0.1.4',
    'description': 'Useful middlewares and clients to use Ory products in flask App',
    'long_description': None,
    'author': 'Andrew Minkin',
    'author_email': 'minkin.andrew@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
