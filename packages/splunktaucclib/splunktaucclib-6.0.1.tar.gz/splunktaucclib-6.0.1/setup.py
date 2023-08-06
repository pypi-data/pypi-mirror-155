# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splunktaucclib',
 'splunktaucclib.common',
 'splunktaucclib.data_collection',
 'splunktaucclib.global_config',
 'splunktaucclib.modinput_wrapper',
 'splunktaucclib.rest_handler',
 'splunktaucclib.rest_handler.endpoint',
 'splunktaucclib.splunk_aoblib']

package_data = \
{'': ['*']}

install_requires = \
['PySocks>=1.7.1,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'solnlib>=4.0.0,<5.0.0',
 'splunk-sdk>=1.6.16,<2.0.0',
 'splunktalib>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'splunktaucclib',
    'version': '6.0.1',
    'description': '',
    'long_description': None,
    'author': 'rfaircloth-splunk',
    'author_email': 'rfaircloth@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
