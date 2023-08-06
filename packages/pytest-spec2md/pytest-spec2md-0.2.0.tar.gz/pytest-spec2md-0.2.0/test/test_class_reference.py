import os

import pytest


@pytest.fixture
def pytester_reference(request, pytester):
    test_data_dir = os.path.join(request.config.rootdir, 'pytester_cases', 'case_class_reference')

    pytester.syspathinsert(os.path.join(request.config.rootdir, 'pytest_spec2md'))

    with open(os.path.join(request.config.rootdir, 'pytester_cases', 'conftest.py')) as file_content:
        source = "".join(file_content.readlines())
        pytester.makeconftest(source=source)

    with open(os.path.join(test_data_dir, 'test_class_reference.py')) as file_content:
        source = "".join(file_content.readlines())
        pytester.makepyfile(source)

    return pytester


def test_runs_1_successful_tests(pytester_reference: pytest.Pytester):
    result = pytester_reference.runpytest("--spec2md")
    print(result.stderr)
    result.assert_outcomes(passed=1)


def test_creates_18_lines_of_documentation(pytester_reference: pytest.Pytester):
    pytester_reference.runpytest("--spec2md")

    with open(os.path.join(pytester_reference.path, 'documentation/spec.md')) as spec:
        spec = spec.readlines()

    assert len(spec) == 18


