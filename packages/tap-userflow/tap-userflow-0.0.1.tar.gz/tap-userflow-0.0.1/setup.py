# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_userflow', 'tap_userflow.tests']

package_data = \
{'': ['*'], 'tap_userflow': ['schemas/*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['tap-userflow = tap_userflow.tap:TapUserFlow.cli']}

setup_kwargs = {
    'name': 'tap-userflow',
    'version': '0.0.1',
    'description': '`tap-userflow` is a Singer tap for UserFlow, built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'Ilkka Peltola',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
