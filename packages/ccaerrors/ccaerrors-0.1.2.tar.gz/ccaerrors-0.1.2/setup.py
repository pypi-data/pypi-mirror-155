# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ccaerrors']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ccaerrors',
    'version': '0.1.2',
    'description': 'universal error handling for python functions.',
    'long_description': '# ccaerrors\n\nUniversal error handling for python functions.\n\n## Usage\n\n```\nimport sys\n\nfrom ccaerrors import errorNotify\n\ndef somefunction():\n    try:\n        pass\n    except Exception as e:\n        errorNotify(sys.exc_info()[2], e)\n\n```\n\n### `errorNotify`\n\nprint the function name and the Exception details to stdout.\n\n### `errorRaise`\n\nprint the function name and the Exception details to stdout and also re-raise the Exception\n\n### `errorExit`\n\nprint the function name and the Exception details to stdout. Exit the script by calling `sys.exit()`.\n',
    'author': 'ccdale',
    'author_email': 'chris.charles.allison+ccaerrors@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ccdale/ccaerrors.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
