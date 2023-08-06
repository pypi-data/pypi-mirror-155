# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tapdance']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'dock-r>=0.2.0,<0.3.0',
 'docker>=4.4.1,<5.0.0',
 'fire>=0.4.0,<0.5.0',
 'importlib-metadata>=3.4.0,<4.0.0',
 'logless>=0.2.1,<0.3.0',
 'runnow>=0.1.0.14,<0.2.0',
 'uio>=0.2.0,<0.3.0']

extras_require = \
{'aws': ['boto3>=1.17.5,<2.0.0', 's3fs<0.5.2'],
 'azure': ['azure-storage-blob>=12.7.1,<13.0.0',
           'azure-storage-file-datalake>=12.2.3,<13.0.0']}

entry_points = \
{'console_scripts': ['tapdance = tapdance.cli:main']}

setup_kwargs = {
    'name': 'tapdance',
    'version': '0.9.9.dev277',
    'description': 'Tapdance is an orchestration layer for the open source Singer tap platform.',
    'long_description': None,
    'author': 'AJ Steers',
    'author_email': 'aj.steers@slalom.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
