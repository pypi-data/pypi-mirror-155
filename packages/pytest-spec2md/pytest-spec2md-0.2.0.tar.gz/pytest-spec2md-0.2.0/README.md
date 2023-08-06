# pytest-spec2md

This project is an add-on to pytest. It generates a markdown file as specification, while running the tests.

This project is inspired by [pytest-spec](https://github.com/pchomik/pytest-spec).

## Getting started

Install the module using pip.

```
pip install pytest-spec2md
```

Then you can activate the module using *--spec* Parameter when calling pytest. You find the generated markdown file
under *documentation/spec.md*.

## Configuration

You can change the target directory using the parameter *spec_target_file*.

```ini
[pytest]
spec_target_file = path/to/target/doc/file
```

## Using markers

The plugin provides the marker *spec_reference*. This marker can be used to connect a test_case with the testing object.
The name of testing object will than be added to the documentation. If an optional documentation is provided, this will
also be displayed.

The marker can be used at every layer of testing object, so you can also use it at a class.

#### Example

```python
import pytest


def function_to_ref():
    """ Simple doc comment
    with two lines
    """
    pass


@pytest.mark.spec_reference(function_to_ref.__name__, function_to_ref.__doc__)
def test_use_a_reference_in_doc():
    assert True
```

## Examples

Examples for the usage can be found here:
[UseCases on GitHub](https://github.com/mh7d/pytest-spec2md/tree/main/pytester_cases)
