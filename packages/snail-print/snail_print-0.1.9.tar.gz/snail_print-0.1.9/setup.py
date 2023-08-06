# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snail_print']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snail-print',
    'version': '0.1.9',
    'description': 'A print funtion that slowly shows the output in console in real time',
    'long_description': '# Snail Print\n\n[![GitHub release][release-image]][release-url]\n[![codeclimate][codeclimate-image]][codeclimate-url]\n![Tests & Linter][ci-url]\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\nThis library includes a print funtion that slows down the showing of output in console, character by character, as though typed by a typewriter.\n\n\n## Getting started\n\nInstall the library with:\n\n```sh\npip install -U snail_print\n```\n\n### Usage\n\n![Presentation Demo Video](https://raw.githubusercontent.com/Baelfire18/snail_print/master/assets/presentacion_color.gif)\n\n*Gif 1: Example of use of this real time print library*\n\nMoreover, every console log in this video was made with the library and with [this file](https://github.com/Baelfire18/snail_print/master/presentation.py)\n\nCopy and paste this code and try it yourself!\n\n```python\nfrom snail_print import snail_print\nsnail_print("Hello World", delay=0.2)\n```\n\n## Documentation\n\n### snail_print\n\n```python\nfunction snail_print(*objects, delay=0.1, sep=" ", end="\\n")\n```\n\n#### Parameters\n\n+ `objects`: Can be any or even multiple python objects.\n\nThe objects whose string representation will be "snail printed".\n\n+ `delay`: `float` or `int`, default `0.1`.\n\nThe delay, measured in seconds, between the printing of each character in `object`.\n\n+ `sep`: `str`, default `" "`.\n\nIn case of having multiple arguments, one sep will be placed between each and the next.\n\n+ `end`: `str`, default `"\\n"`.\n\nThe final character of the print. By default creates a new line.\n\n\n## Testing\n\nRun the test suite with:\n\n```sh\npython -m unittest tests\n```\n\n## Install local\n\nTo install it locally from the source code:\n\n```sh\npython setup.py develop\n```\n\n[release-image]: https://img.shields.io/github/v/release/Baelfire18/snail_print.svg\n[release-url]: https://github.com/Baelfire18/snail_print/releases/latest\n[codeclimate-image]: https://codeclimate.com/github/Baelfire18/snail_print/badges/gpa.svg\n[codeclimate-url]: https://codeclimate.com/github/Baelfire18/snail_print\n[ci-url]: https://github.com/Baelfire18/snail_print/actions/workflows/tests-and-linter.yml/badge.svg\n',
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
