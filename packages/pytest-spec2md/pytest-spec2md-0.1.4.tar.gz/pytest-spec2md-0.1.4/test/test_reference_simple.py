import os

import pytest


@pytest.fixture
def pytester_reference(request, pytester):
    test_data_dir = os.path.join(request.config.rootdir, 'pytester_cases', 'case_reference_simple')

    pytester.syspathinsert(os.path.join(request.config.rootdir, 'pytest_spec2md'))

    with open(os.path.join(request.config.rootdir, 'pytester_cases', 'conftest.py')) as file_content:
        source = "".join(file_content.readlines())
        pytester.makeconftest(source=source)

    with open(os.path.join(test_data_dir, 'test_ref.py')) as file_content:
        source = "".join(file_content.readlines())
        pytester.makepyfile(source)

    return pytester


def test_runs_1_successful_tests(pytester_reference: pytest.Pytester):
    result = pytester_reference.runpytest("--spec2md")
    result.assert_outcomes(passed=1)


def test_creates_12_lines_of_documentation(pytester_reference: pytest.Pytester):
    pytester_reference.runpytest("--spec2md")

    with open(os.path.join(pytester_reference.path, 'documentation/spec.md')) as spec:
        spec = spec.readlines()

    assert len(spec) == 12


def test_contains_referenced_func_name_in_spec(pytester_reference: pytest.Pytester):
    pytester_reference.runpytest("--spec2md")

    with open(os.path.join(pytester_reference.path, 'documentation/spec.md')) as spec:
        spec = spec.readlines()

    assert any(x.find('function_to_ref') >= 0 for x in spec)
