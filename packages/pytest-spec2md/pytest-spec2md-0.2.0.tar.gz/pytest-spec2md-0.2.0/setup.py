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
    'version': '0.2.0',
    'description': 'Library pytest-spec2md is a pytest plugin to create a markdown specification while running pytest.',
    'long_description': '# pytest-spec2md\n\nThis project is an add-on to pytest. It generates a markdown file as specification, while running the tests.\n\nThis project is inspired by [pytest-spec](https://github.com/pchomik/pytest-spec).\n\n## Getting started\n\nInstall the module using pip.\n\n```\npip install pytest-spec2md\n```\n\nThen you can activate the module using *--spec* Parameter when calling pytest. You find the generated markdown file\nunder *documentation/spec.md*.\n\n## Configuration\n\nYou can change the target directory using the parameter *spec_target_file*.\n\n```ini\n[pytest]\nspec_target_file = path/to/target/doc/file\n```\n\n## Using markers\n\nThe plugin provides the marker *spec_reference*. This marker can be used to connect a test_case with the testing object.\nThe name of testing object will than be added to the documentation. If an optional documentation is provided, this will\nalso be displayed.\n\nThe marker can be used at every layer of testing object, so you can also use it at a class.\n\n#### Example\n\n```python\nimport pytest\n\n\ndef function_to_ref():\n    """ Simple doc comment\n    with two lines\n    """\n    pass\n\n\n@pytest.mark.spec_reference(function_to_ref.__name__, function_to_ref.__doc__)\ndef test_use_a_reference_in_doc():\n    assert True\n```\n\n## Examples\n\nExamples for the usage can be found here:\n[UseCases on GitHub](https://github.com/mh7d/pytest-spec2md/tree/main/pytester_cases)\n',
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
