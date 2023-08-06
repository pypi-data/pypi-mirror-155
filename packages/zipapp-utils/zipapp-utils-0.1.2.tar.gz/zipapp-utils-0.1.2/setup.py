# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zipapp_utils']

package_data = \
{'': ['*'], 'zipapp_utils': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0']

entry_points = \
{'console_scripts': ['zipapp-utils = zipapp_utils.cli:main']}

setup_kwargs = {
    'name': 'zipapp-utils',
    'version': '0.1.2',
    'description': 'zipapp utilities',
    'long_description': '',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tddschn/zipapp-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
