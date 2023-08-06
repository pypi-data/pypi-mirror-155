# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rin_exceptions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rin-exceptions',
    'version': '1.0.0',
    'description': 'A set of base exceptions for Rin',
    'long_description': '<div align="center">\n\n# Rin-Exceptions\n\n![Rin](https://raw.githubusercontent.com/No767/Rin/dev/assets/Rin%20Logo%20V4%20(GitHub).png)\n\n\n![PyPI](https://img.shields.io/pypi/v/rin-exceptions?label=PyPi&logo=pypi&logoColor=white) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rin-exceptions?label=Python&logo=python&logoColor=white) ![PyPI - Downloads](https://img.shields.io/pypi/dd/rin-exceptions?label=PyPi%20Downloads&logo=pypi&logoColor=white) ![GitHub](https://img.shields.io/github/license/No767/Rin-Exceptions?label=License&logo=github)\n\nA set of base exceptions for Rin\n\n<div align="left">\n\n# Info\n\nThis package is a set of base exceptions used by Rin. It\'s meant to contain custom exceptions that are used by Rin, and in turn, Kumiko.\n\n# Installation\n\npip: \n\n```sh\npip install rin-exceptions\n```\n\npoetry:\n\n```sh\npoetry add rin-exceptions\n```',
    'author': 'No767',
    'author_email': '73260931+No767@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/No767/Rin-Exceptions',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
