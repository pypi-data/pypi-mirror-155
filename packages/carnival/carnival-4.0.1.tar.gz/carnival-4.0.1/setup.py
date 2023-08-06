# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carnival',
 'carnival.contrib',
 'carnival.contrib.steps',
 'carnival.contrib.steps.systemd',
 'carnival.contrib.steps.systemd.journald',
 'carnival.hosts',
 'carnival.hosts.base',
 'carnival.hosts.local',
 'carnival.hosts.ssh',
 'carnival.steps']

package_data = \
{'': ['*']}

install_requires = \
['Click==8.0.3',
 'Jinja2==3.0.3',
 'colorama>=0.4.4,<0.5.0',
 'paramiko>=2.8.1,<3.0.0',
 'python-dotenv==0.19.2',
 'tqdm>=4.62.3,<5.0.0']

entry_points = \
{'console_scripts': ['carnival = carnival.cli:main']}

setup_kwargs = {
    'name': 'carnival',
    'version': '4.0.1',
    'description': 'Software provisioning tool',
    'long_description': None,
    'author': 'Dmirty Simonov',
    'author_email': 'demalf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
