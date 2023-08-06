# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snail_print']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snail-print',
    'version': '0.1.6',
    'description': 'A print funtion that slowly shows the output in console in real time',
    'long_description': '# Snail Print\n\n[![GitHub release](https://img.shields.io/github/v/release/Baelfire18/slow_print.svg)](../../releases/latest)\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\nThis library includes a print funtion that slowly shows the output in console in real time.\n\n\n\nMoreover, every console log in this video was made with the library and with [this file](https://github.com/Baelfire18/snail_print/master/presentation.py)\n\n## Getting started\n\nInstall the library with:\n\n```sh\npip install -U snail_print\n```\n\n### Usage\n\n![Presentation Demo Video](https://raw.githubusercontent.com/Baelfire18/snail_print/master/assets/presentacion_color.gif)\n\n*Video 1: Example of use of this real life print library*\n\n## Documentation\n\n### snail_print\n\n```python\nfunction snail_print(*objects, delay=0.1, sep=" ", end="\\n", flush=False)\n```\n\n#### Parameters\n\n+ `objects`: Can be any python object.\n\nThe object wicth will be printed slowly in real time.\n\n+ `delay`: `float` or `int`, default `0.1`.\n\nThe time between the addition in console of the next character.\n\n+ `sep`: `str`, default `" "`.\n\nIn case of having mutiple arguments this may be separated by this string.\n\n+ `end`: `str`, default `"\\n"`.\n\nThe final character of the print. By default creates a new line.\n\n\n## Testing\n\nRun the test suite with:\n\n```sh\npython -m unittest tests\n```\n\n## Install Local\n\nTo install it locally from the source code:\n\n```sh\npython setup.py develop\n```\n',
    'author': 'Jose Antonio Castro',
    'author_email': 'jacastro18@uc.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Baelfire18/snail_print',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
