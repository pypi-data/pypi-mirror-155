# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['shrub', 'shrub.v2', 'shrub.v3']

package_data = \
{'': ['*']}

install_requires = \
['PyYaml>=5.1,<6.0',
 'git-url-parse>=1,<2',
 'pydantic>=1.8,<2.0',
 'typing-extensions>=4,<5']

extras_require = \
{':python_full_version >= "3.6.0" and python_full_version < "3.7.0"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'shrub.py',
    'version': '3.0.3',
    'description': 'Library for creating evergreen configurations',
    'long_description': '# shrub.py\n\nA python based Evergreen project config generation library\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shrub.py)\n[![PyPI version](https://badge.fury.io/py/shrub.py.svg)](https://pypi.org/project/shrub.py/)\n\n## Overview\n\nBased on [shrub](https://github.com/evergreen-ci/shrub/), shrub.py is a library for programatically\nbuilding Evergreen project configurations described [here](https://github.com/evergreen-ci/evergreen/wiki/Project-Files).\n\n## Example\n\nThe following snippet will create a set of parallel tasks reported under a single display task. It\nwould generate json used by ```generate.tasks```:\n\n```\nfrom shrub.v2 import ShrubProject, Task, BuildVariant\n\nn_tasks = 10\ndef define_task(index):\n    name = f"task_name_{index}"\n\n    return Task(\n        name,\n        [\n            FunctionCall("do setup"),\n            FunctionCall(\n                "run test generator",\n                {"parameter_1": "value 1", "parameter_2": "value 2"}\n            ),\n            FunctionCall("run tests")\n        ],\n    ).dependency("compile")\n\ntasks = {define_task(i) for i in range(n_tasks)}\nvariant = BuildVariant("linux-64").display_task("test_suite", tasks)\nproject = ShrubProject({variant})\n\nproject.json()\n```\n\n## Run tests\n\n```\npoetry run pytest\n```\n',
    'author': 'David Bradford',
    'author_email': 'david.bradford@mongodb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/evergreen-ci/shrub.py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>3.6.1',
}


setup(**setup_kwargs)
