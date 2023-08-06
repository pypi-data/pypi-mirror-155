# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sep_text']

package_data = \
{'': ['*']}

install_requires = \
['fastlid>=0.1.7,<0.2.0',
 'icecream>=2.1.1,<3.0.0',
 'install>=1.3.5,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'set-loglevel>=0.1.2,<0.2.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['sep-text = sep_text.__main__:app']}

setup_kwargs = {
    'name': 'sep-text',
    'version': '0.1.0',
    'description': 'Separate two texts, paragraph by paragraph',
    'long_description': '# sep-text\n[![pytest](https://github.com/ffreemt/sep-text/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/sep-text/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/sep_text.svg)](https://badge.fury.io/py/sep_text)\n\nSeparate two texts, paragraph by paragraph\n\n## Install it\n\n```shell\npip install sep-text\n\n# pip install git+https://github.com/ffreemt/sep-text\n# poetry add git+https://github.com/ffreemt/sep-text\n# git clone https://github.com/ffreemt/sep-text && cd sep-text\n```\n\nIf your environment does not have a C compiler, install fasttext.whl first. You can find fasttext.whl from [https://www.lfd.uci.edu/~gohlke/pythonlibs/](https://www.lfd.uci.edu/~gohlke/pythonlibs/).\n\n## Use it\n```python\nfrom sep_text import sep_text\n\nprint(sep_text("This is a text\\nMachen wir etwas"))\n# (\'Machen wir etwas\', \'This is a text\')\n\nprint(sep_text.langs)\n# [\'de\', \'en\']\n\nprint(sep_text.conf)\n# [0.994, 0.004]\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/sep-text',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
