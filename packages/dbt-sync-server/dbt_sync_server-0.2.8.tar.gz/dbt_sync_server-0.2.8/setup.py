# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dbt_sync_server']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1,<2',
 'Werkzeug<2',
 'click>=8.0.4,<9.0.0',
 'dbt-core>1.0.1',
 'dbt-rpc>=0.1.1,<0.2.0',
 'itsdangerous==2.0.1']

entry_points = \
{'console_scripts': ['dbt-sync-server = dbt_sync_server:cli']}

setup_kwargs = {
    'name': 'dbt-sync-server',
    'version': '0.2.8',
    'description': 'Server which abstracts RPC and simplifies SQL execution and compilation',
    'long_description': None,
    'author': 'Alex Butler',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
