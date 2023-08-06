import os

import pytest
import xml.etree.ElementTree as et


@pytest.fixture
def pytester_advanced(request, pytester):
    test_data_dir = os.path.join(request.config.rootdir, 'pytester_cases', 'case_advanced')

    pytester.syspathinsert(os.path.join(request.config.rootdir, 'pytest_spec2md'))

    with open(os.path.join(request.config.rootdir, 'pytester_cases', 'conftest.py')) as file_content:
        source = "".join(file_content.readlines())
        pytester.makeconftest(source=source)

    with open(os.path.join(test_data_dir, 'test_advanced.py')) as file_content:
        source = "".join(file_content.readlines())
        pytester.makepyfile(source)

    return pytester


def test_runs_6_successful_tests(pytester_advanced: pytest.Pytester):
    result = pytester_advanced.runpytest("--spec2md")
    result.assert_outcomes(passed=6)


def test_creates_27_lines_of_documentation(pytester_advanced: pytest.Pytester):
    pytester_advanced.runpytest("--spec2md")

    with open(os.path.join(pytester_advanced.path, 'documentation/spec.md')) as spec:
        spec = spec.readlines()

    assert len(spec) == 27


def test_generates_sub_class_heading_entry(pytester_advanced: pytest.Pytester):
    pytester_advanced.runpytest("--spec2md")

    with open(os.path.join(pytester_advanced.path, 'documentation/spec.md')) as spec:
        spec = spec.readlines()

    assert '#### Sub Class\n' in spec


def test_junitxml_creates_6_testcases(pytester_advanced: pytest.Pytester):
    pytester_advanced.runpytest("--spec2md", "--junitxml=junit.xml")

    root_node = et.parse(os.path.join(pytester_advanced.path, 'junit.xml')).getroot()
    test_cases = root_node.findall('.//*')
    assert sum(x.tag == 'testsuite' for x in test_cases) == 1
    assert sum(x.tag == 'testcase' for x in test_cases) == 6
    assert all(x.attrib.get('name', '') for x in test_cases)
