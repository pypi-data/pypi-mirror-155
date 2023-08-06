# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['repo_autoindex']

package_data = \
{'': ['*'], 'repo_autoindex': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'aiohttp>=3.8.1,<4.0.0', 'defusedxml>=0.7.1,<0.8.0']

entry_points = \
{'console_scripts': ['repo-autoindex = repo_autoindex.cmd:entrypoint']}

setup_kwargs = {
    'name': 'repo-autoindex',
    'version': '0.1.0',
    'description': 'Generic static HTML indexes of various repository types',
    'long_description': None,
    'author': 'Rohan McGovern',
    'author_email': 'rmcgover@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
