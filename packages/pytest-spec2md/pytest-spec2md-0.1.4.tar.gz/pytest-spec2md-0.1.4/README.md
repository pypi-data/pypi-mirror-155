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

## Examples

Examples for the usage can be found here: 
[UseCases on GitHub](https://github.com/mh7d/pytest-spec2md/tree/main/pytester_cases)
