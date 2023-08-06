# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['smartapp']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'attrs>=21.4.0,<22.0.0',
 'cattrs>=22.1.0,<23.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pycryptodomex>=3.14.1,<4.0.0',
 'requests>=2.28.0,<3.0.0',
 'tenacity>=8.0.1,<9.0.0']

setup_kwargs = {
    'name': 'smartapp-sdk',
    'version': '0.1.0',
    'description': 'Framework to build a webhook-based SmartThings SmartApp',
    'long_description': "# SmartApp SDK\n\n[![pypi](https://img.shields.io/pypi/v/smartapp-sdk.svg)](https://pypi.org/project/smartapp-sdk/)\n[![license](https://img.shields.io/pypi/l/smartapp-sdk.svg)](https://github.com/pronovic/smartapp-sdk/blob/master/LICENSE)\n[![wheel](https://img.shields.io/pypi/wheel/smartapp-sdk.svg)](https://pypi.org/project/smartapp-sdk/)\n[![python](https://img.shields.io/pypi/pyversions/smartapp-sdk.svg)](https://pypi.org/project/smartapp-sdk/)\n[![Test Suite](https://github.com/pronovic/smartapp-sdk/workflows/Test%20Suite/badge.svg)](https://github.com/pronovic/smartapp-sdk/actions?query=workflow%3A%22Test+Suite%22)\n[![docs](https://readthedocs.org/projects/smartapp-sdk/badge/?version=stable&style=flat)](https://smartapp-sdk.readthedocs.io/en/stable/)\n[![coverage](https://coveralls.io/repos/github/pronovic/smartapp-sdk/badge.svg?branch=master)](https://coveralls.io/github/pronovic/smartapp-sdk?branch=master)\n\nsmartapp-sdk is a Python library to build a [webhook-based SmartApp](https://developer-preview.smartthings.com/docs/connected-services/smartapp-basics/) for the [SmartThings platform](https://www.smartthings.com/).\n\nThe SDK is intended to be easy to use no matter how you choose to structure your code, whether that's a traditional Python webapp (such as FastAPI on Uvicorn) or a serverless application (such as AWS Lambda).\n\nThe SDK handles all the mechanics of the [webhook lifecycle interface](https://developer-preview.smartthings.com/docs/connected-services/lifecycles/) on your behalf.  You just implement a single endpoint to accept the SmartApp webhook requests, and a single callback class where you define specialized behavior for the webhook events.  A clean [attrs](https://www.attrs.org/en/stable/) object interface is exposed for use by your callback.\n\nSDK documentation is found at [smartapp-sdk.readthedocs.io](https://smartapp-sdk.readthedocs.io/en/stable/).  Look there for installation instructions, the class model documentation, and example code.\n",
    'author': 'Kenneth J. Pronovici',
    'author_email': 'pronovic@ieee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/smartapp-sdk/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
