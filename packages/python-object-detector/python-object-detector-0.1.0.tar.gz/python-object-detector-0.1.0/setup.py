# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.object_detector', 'src.object_detector.yolo']

package_data = \
{'': ['*'], 'src.object_detector': ['data/*']}

install_requires = \
['filetype>=1.0.13,<2.0.0',
 'numpy>=1.22.4,<2.0.0',
 'opencv-python>=4.6.0,<5.0.0']

setup_kwargs = {
    'name': 'python-object-detector',
    'version': '0.1.0',
    'description': 'Python object detector for aerial detection.',
    'long_description': '# python-object-detector\nGeneric object detector interface for Python\n\nhttps://semver.org/spec/v2.0.0.html\nGiven a version number MAJOR.MINOR.PATCH, increment the:\n\nMAJOR version when you make incompatible API changes,\nMINOR version when you add functionality in a backwards compatible manner, and\nPATCH version when you make backwards compatible bug fixes.\nAdditional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.\n\n# Introduction\n# Installation\n# Usage\n# History\n\n# Development\n```shell\nblack ./src/ ./tests/ .\n```\n```shell\nmypy .\n```\n```shell\npflake8 .\n```',
    'author': 'Cristian Ion',
    'author_email': 'cristian.ion94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cristianion94/python-object-detector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
