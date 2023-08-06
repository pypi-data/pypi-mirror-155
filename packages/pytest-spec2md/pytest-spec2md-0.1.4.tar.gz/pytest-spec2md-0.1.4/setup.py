# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_spec2md', 'test']

package_data = \
{'': ['*']}

install_requires = \
['pytest>7.0', 'six']

entry_points = \
{'pytest11': ['pytest_spec = pytest_spec2md.plugin']}

setup_kwargs = {
    'name': 'pytest-spec2md',
    'version': '0.1.4',
    'description': 'Library pytest-spec2md is a pytest plugin to create a markdown specification while running pytest.',
    'long_description': '# pytest-spec2md\n\nThis project is an add-on to pytest. It generates a markdown file as specification, while running the tests.\n\nThis project is inspired by [pytest-spec](https://github.com/pchomik/pytest-spec).\n\n## Getting started\n\nInstall the module using pip.\n\n```\npip install pytest-spec2md\n```\n\nThen you can activate the module using *--spec* Parameter when calling pytest. You find the generated markdown file\nunder *documentation/spec.md*.\n\n## Configuration\n\nYou can change the target directory using the parameter *spec_target_file*.\n\n```ini\n[pytest]\nspec_target_file = path/to/target/doc/file\n```\n\n## Examples\n\nExamples for the usage can be found here: \n[UseCases on GitHub](https://github.com/mh7d/pytest-spec2md/tree/main/pytester_cases)\n',
    'author': 'mh7d',
    'author_email': None,
    'maintainer': 'mh7d',
    'maintainer_email': None,
    'url': 'https://github.com/mh7d/pytest-spec2md',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.8',
}


setup(**setup_kwargs)
