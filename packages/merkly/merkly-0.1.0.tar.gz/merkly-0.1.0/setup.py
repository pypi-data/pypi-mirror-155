# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['merkly']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'merkly',
    'version': '0.1.0',
    'description': '🌳 The simple and easy implementation of Merkle Tree',
    'long_description': '# 🌳 Merkly\n\nThe **simple and easy** implementation of **Python Merkle Tree**\n\n---\n\n[![Test](https://github.com/olivmath/merkly/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/olivmath/merkly/actions/workflows/test.yml)\n![GitHub last commit](https://img.shields.io/github/last-commit/olivmath/merkly)\n![GitHub commit activity](https://img.shields.io/github/commit-activity/m/olivmath/merkly)\n\n![PyPI](https://img.shields.io/pypi/v/merkly)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/merkly)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/merkly)\n![PyPI - License](https://img.shields.io/pypi/l/merkly)\n\n## CREDITS\n\n[![GitHub Contributors Image](https://contrib.rocks/image?repo=olivmath/merkly)](https://github.com/olivmath/merkly/graphs/contributors)\n\n## HOW TO INSTALL\n\n```\npoetry add merkly\n```\n\n```\npip install merkly\n```\n\n## HOW IT WORKS\n\nThis library provides a clean and easy to use implementation of the Merkle Tree with the following features:\n\n- [x] Create Leaf\n- [ ] Create Root\n- [ ] Create Proof\n- [ ] Validate Leafs\n\n## CONTRIBUTING\n\nFollow the guide of development -> [CONTRIBUTING](CONTRIBUTING.md)\n\n## LICENSE\n\n[MIT](LICENSE)\n',
    'author': 'Lucas Oliveira',
    'author_email': 'olivmath@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
