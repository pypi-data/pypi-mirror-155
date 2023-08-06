# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jiren']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=3.0,<4.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['jiren = jiren.cli:main']}

setup_kwargs = {
    'name': 'jiren',
    'version': '0.4.0',
    'description': 'jinja2 template renderer',
    'long_description': '# jiren\n\njiren is an application that generates text from a template. The format of the template is based on jinja2.\n\n[![PyPI](https://img.shields.io/pypi/v/jiren.svg)](https://pypi.org/project/jiren/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jiren.svg)](https://pypi.org/project/jiren/)\n[![Python Tests](https://github.com/speg03/jiren/workflows/Python%20Tests/badge.svg)](https://github.com/speg03/jiren/actions?query=workflow%3A%22Python+Tests%22)\n[![codecov](https://codecov.io/gh/speg03/jiren/branch/main/graph/badge.svg)](https://codecov.io/gh/speg03/jiren)\n\nRead this in Japanese: [日本語](https://github.com/speg03/jiren/blob/main/README.ja.md)\n\n## Installation\n\n```sh\npip install jiren\n```\n\n## Usage\n\n### Generate text\n\nGenerate text from a template using the `jiren` command. This command can read a template from stdin or files.\n\nAn example of reading a template from stdin:\n\nCommand:\n```sh\necho "hello, {{ name }}" | jiren --input=- -- --name=world\n```\nOutputs:\n```\nhello, world\n```\n\nAn example of reading a template from a file:\n\nCommand:\n```sh\ncat <<EOF >template.j2\nhello, {{ name }}\nEOF\n\njiren --input=template.j2 -- --name=world\n```\nOutputs:\n```\nhello, world\n```\n\nIn this example, the template contains a variable called `name`. You can set values for variables in a template using program arguments passed to the `jiren` command. Note that the arguments for the variables must be located after `--`.\n\nIf you want to know more about template format, please refer to jinja2 document ( http://jinja.pocoo.org/ ).\n\n\n### Variables in a template\n\nYou can use the help to check the variables defined in a template.\n\nCommand:\n```sh\necho "{{ greeting }}, {{ name }}" | jiren --input=- --help\n```\nOutputs:\n```\n... (omitted)\n\nvariables:\n  --name NAME\n  --greeting GREETING\n```\n\n\n### Default values\n\nYou can set default values for variables for which no values was specified. This is based on the jinja2 specification.\n\nCommand:\n```sh\necho "{{ greeting }}, {{ name | default(\'world\') }}" | jiren --input=- -- --greeting=hello\n```\nOutputs:\n```\nhello, world\n```\n\n\n### Option: required\n\nWhen using the `--required` option, you must specify values for all variables.\n\nCommand:\n```sh\necho "{{ greeting }}, {{ name }}" | jiren --input=- --required -- --greeting=hello\n```\nOutputs:\n```\njiren: error: the following arguments are required: --name\n```\n',
    'author': 'Takahiro Yano',
    'author_email': 'speg03@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/speg03/jiren',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
