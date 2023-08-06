# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brown']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'brown',
    'version': '0.0.1',
    'description': '',
    'long_description': '# brown\n\n[![PyPI](https://img.shields.io/pypi/v/brown)](https://pypi.org/project/brown/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/brown)](https://www.python.org/downloads/)\n[![GitHub last commit](https://img.shields.io/github/last-commit/daxartio/brown)](https://github.com/daxartio/brown)\n[![GitHub stars](https://img.shields.io/github/stars/daxartio/brown?style=social)](https://github.com/daxartio/brown)\n\n```\npip install brown\n```\n\n## Contributing\n\n[Contributing](CONTRIBUTING.md)\n',
    'author': 'Danil Akhtarov',
    'author_email': 'daxartio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/brown',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
