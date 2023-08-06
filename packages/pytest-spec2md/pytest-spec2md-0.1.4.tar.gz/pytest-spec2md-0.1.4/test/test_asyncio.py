import os

import pytest
import xml.etree.ElementTree as et


@pytest.fixture
def pytester_asyncio(request, pytester):
    test_data_dir = os.path.join(request.config.rootdir, 'pytester_cases', 'case_asyncio')

    pytester.syspathinsert(os.path.join(request.config.rootdir, 'pytest_spec2md'))

    with open(os.path.join(request.config.rootdir, 'pytester_cases', 'conftest.py')) as file_content:
        source = "".join(file_content.readlines())
        pytester.makeconftest(source=source)

    with open(os.path.join(test_data_dir, 'test_simple.py')) as file_content:
        source = "".join(file_content.readlines())
        pytester.makepyfile(source)

    return pytester


def test_simple_runs_4_successful_tests(pytester_asyncio: pytest.Pytester):
    result = pytester_asyncio.runpytest("--spec2md")
    result.assert_outcomes(passed=4)


def test_spec_created_using_junit_and_cov(pytester_asyncio: pytest.Pytester):
    pytester_asyncio.runpytest("--spec2md", "--junitxml=junit.xml")

    assert os.path.exists(os.path.join(pytester_asyncio.path, 'documentation/spec.md'))


def test_junitxml_creates_4_testcases(pytester_asyncio: pytest.Pytester):
    pytester_asyncio.runpytest("--spec2md", "--junitxml=junit.xml")

    root_node = et.parse(os.path.join(pytester_asyncio.path, 'junit.xml')).getroot()
    test_cases = root_node.findall('.//*')

    assert sum(x.tag == 'testsuite' for x in test_cases) == 1

    # see: https://github.com/pytest-dev/pytest-asyncio/issues/369 generates 5 instead of 4
    assert sum(x.tag == 'testcase' for x in test_cases) == 5


