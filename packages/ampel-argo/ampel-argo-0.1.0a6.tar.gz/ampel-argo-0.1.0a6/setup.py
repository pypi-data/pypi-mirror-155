# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ampel', 'ampel.argo']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.3.0,<3.0.0',
 'ampel-core>=0.8.2-alpha.13,<0.8.3',
 'fastapi>=0.75.0,<0.76.0',
 'httpx>=0.22.0,<0.23.0',
 'uvicorn>=0.17.6,<0.18.0']

entry_points = \
{'console_scripts': ['ampel-argo-render = ampel.argo.job:entrypoint']}

setup_kwargs = {
    'name': 'ampel-argo',
    'version': '0.1.0a6',
    'description': '',
    'long_description': None,
    'author': 'Jakob van Santen',
    'author_email': 'jvansanten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
