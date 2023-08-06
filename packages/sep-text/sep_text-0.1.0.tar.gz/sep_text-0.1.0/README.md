# sep-text
[![pytest](https://github.com/ffreemt/sep-text/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/sep-text/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/sep_text.svg)](https://badge.fury.io/py/sep_text)

Separate two texts, paragraph by paragraph

## Install it

```shell
pip install sep-text

# pip install git+https://github.com/ffreemt/sep-text
# poetry add git+https://github.com/ffreemt/sep-text
# git clone https://github.com/ffreemt/sep-text && cd sep-text
```

If your environment does not have a C compiler, install fasttext.whl first. You can find fasttext.whl from [https://www.lfd.uci.edu/~gohlke/pythonlibs/](https://www.lfd.uci.edu/~gohlke/pythonlibs/).

## Use it
```python
from sep_text import sep_text

print(sep_text("This is a text\nMachen wir etwas"))
# ('Machen wir etwas', 'This is a text')

print(sep_text.langs)
# ['de', 'en']

print(sep_text.conf)
# [0.994, 0.004]
```
