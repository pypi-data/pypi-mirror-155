# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-grit',
    'version': '0.0.1a0',
    'description': 'Exception handling context manager.',
    'long_description': '# grit\n\n[![ci](https://github.com/Kilo59/grit/workflows/ci/badge.svg)](https://github.com/Kilo59/grit/actions)\n[![pypi version](https://img.shields.io/pypi/v/grit.svg)](https://pypi.org/project/grit/)\n![Python Versions](https://img.shields.io/pypi/pyversions/grit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nContext manager for shrugging off exceptions less badly.\n\nSubtitle: exception handling for lazy people.\n\n## Description and Rational\n\nDoes your code suffer from an overuse of bare exceptions?\n\nWhat if you could still shrug off exceptions when needed but not be so cringe about it?\n\n```python\ntry:\n    foobar()\nexcept Exception:\n    pass\n```\n\n```python\nfrom grit import Grit\n\n# Full exception stacktrace is automatically logged\nwith Grit():\n    foobar()\n```\n\n## Quick start\n\n```\npip install py-grit\n```\n\n```python\n>>> from grit import Grit\n>>> with Grit():\n...     raise RunTimeError("something bad")\n>>> print("Uh, everything is under control. Situation normal")\nUh, everything is under control. Situation normal\n\n```\n\nPropagate the errors you care about, while ignoring the ones you don\'t.\n\n```python\n>>> from grit import Grit\n>>> with Grit(dnr_list=[ZeroDivisionError]):\n...     42 / 0\nTraceback (most recent call last):\n    ...\nZeroDivisionError: division by zero\n\n```\n\nAnd handle those that require special attention\n\n```python\n>>> from grit import Grit\n>>> with Grit(handlers={ValueError: print}):\n...     raise ValueError("what have you done?!")\nwhat have you done?!\n\n```\n\n## Logging and results\n\n`Grit()` accepts a `fallback_handler` callable which will be called on the exception if no specific\n\'handler\' (`handlers`) is found.\n\nBy default the `fallback_handler` will log a full exception traceback at the debug level using `self.logger`.\n\nTo change this behavior, provide your own `fallback_handler` or explicitly set it a `None`.\n\n```python\n>>> from grit import Grit\n>>> with Grit(fallback_handler=print):\n...     raise TypeError("what have I done?!")\nwhat have I done?!\n\n```\n\n## Usage Examples\n\nTODO ...\n',
    'author': 'Gabriel Gore',
    'author_email': 'gabriel59kg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kilo59/grit',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
