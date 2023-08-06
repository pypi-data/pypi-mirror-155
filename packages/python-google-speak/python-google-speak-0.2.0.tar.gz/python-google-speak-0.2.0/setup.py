# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_google_speak', 'python_google_speak.test']

package_data = \
{'': ['*'], 'python_google_speak.test': ['data/*']}

install_requires = \
['playsound==1.3.0', 'requests==2.27.1']

entry_points = \
{'console_scripts': ['google_speak = python_google_speak.cli:main']}

setup_kwargs = {
    'name': 'python-google-speak',
    'version': '0.2.0',
    'description': 'Simple class to create speech files using the Google translate URL',
    'long_description': None,
    'author': 'Marcus Rickert',
    'author_email': 'marcus.rickert@web.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
