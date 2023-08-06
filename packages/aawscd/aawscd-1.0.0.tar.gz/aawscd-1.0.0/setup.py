# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aawscd', 'aawscd.tools']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'docopt>=0.6,<0.7',
 'h5py>=3,<4',
 'paho-mqtt>=1.6.1,<2.0.0',
 'pyaaware>=1.3.17,<2.0.0',
 'tqdm>=4.62,<5.0']

entry_points = \
{'console_scripts': ['aawscd_copycat = aawscd.aawscd_copycat:main',
                     'aawscd_getconf = aawscd.aawscd_getconf:main',
                     'aawscd_pdcap = aawscd.aawscd_pdcap:main',
                     'aawscd_probmon = aawscd.aawscd_probmon:main',
                     'aawscd_probwrite = aawscd.aawscd_probwrite:main',
                     'aawscd_setdirection = aawscd.aawscd_setdirection:main',
                     'aawscd_wwclient = aawscd.aawscd_wwclient:main',
                     'aawscd_wwrecord = aawscd.aawscd_wwrecord:main']}

setup_kwargs = {
    'name': 'aawscd',
    'version': '1.0.0',
    'description': 'Utilities for the Aaware Sound Capture platform',
    'long_description': 'aawscd: Utilities for the Aaware Sound Capture platform\n',
    'author': 'Chris Eddington',
    'author_email': 'chris@aaware.com',
    'maintainer': 'Chris Eddington',
    'maintainer_email': 'chris@aaware.com',
    'url': 'https://aaware.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
