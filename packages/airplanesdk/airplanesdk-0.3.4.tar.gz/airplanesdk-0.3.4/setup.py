# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airplane']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.10.0,<2.0.0',
 'deprecation>=2.1.0,<3.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'airplanesdk',
    'version': '0.3.4',
    'description': 'A Python SDK for writing Airplane tasks',
    'long_description': '# Airplane Python SDK [![PyPI](https://img.shields.io/pypi/v/airplanesdk)](https://pypi.org/project/airplanesdk/) [![PyPI - License](https://img.shields.io/pypi/l/airplanesdk)](./LICENSE) [![Docs](https://img.shields.io/badge/Docs-airplane-blue)](https://docs.airplane.dev/creating-tasks/python)\n\nSDK for writing [Airplane](https://airplane.dev) tasks in Python.\n\n## Getting started\n\n```sh\npip install airplanesdk\n```\n\n## Usage\n\nTo write a Python task in Airplane, create a `.py` file and export a function like so:\n\n```py\nimport airplane\n\ndef main(params):\n  return f"Hello, {params[\'name\']}"\n```\n\nYou can configure the parameters that your task will receive in the [Airplane UI](http://app.airplane.dev/). They\'ll be passed through the `params` argument to your function as a dictionary keyed by the slugs you see in the UI.\n\nTo execute your task, first [install the Airplane CLI](https://docs.airplane.dev/platform/airplane-cli).\n\nOnce installed, execute your task locally:\n\n```sh\nairplane dev ./path/to/file.py -- --name=World\n```\n\nIf that looks good, deploy your task to Airplane and give it a [run in the UI](https://app.airplane.dev/library)!\n\n```sh\nairplane deploy ./path/to/file.py\n```\n',
    'author': 'Airplane',
    'author_email': 'support@airplane.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://airplane.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
