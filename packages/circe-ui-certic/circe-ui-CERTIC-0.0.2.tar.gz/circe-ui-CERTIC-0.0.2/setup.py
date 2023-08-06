# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['circe_ui']

package_data = \
{'': ['*'], 'circe_ui': ['static/*']}

install_requires = \
['aiofiles>=0.8.0',
 'argh>=0.26.2',
 'circe-client-CERTIC>=0.0.7',
 'itsdangerous>=2.1.2',
 'python-dotenv>=0.20.0',
 'sanic>=22.3.2']

entry_points = \
{'console_scripts': ['circeui = circe_ui.__main__:run_cli']}

setup_kwargs = {
    'name': 'circe-ui-certic',
    'version': '0.0.2',
    'description': 'Circe Web UI',
    'long_description': None,
    'author': 'Mickaël Desfrênes',
    'author_email': 'mickael.desfrenes@unicaen.fr',
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
