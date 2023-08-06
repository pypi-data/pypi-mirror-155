import os

import _pytest
import _pytest.terminal
import pytest
import inspect

import pytest_spec2md.spec_creator


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        '--spec2md',
        action='store_true',
        dest='spec2md',
        help='Saves test results as specification document in markdown format.'
    )

    parser.addini(
        'spec_target_file',
        default='documentation/spec.md',
        help='The target file to save the generated specification.'
    )

    parser.addini(
        'spec_indent',
        default='  ',
        help='Indention of spec in console.'
    )


default_funcs = {}


def _initialize():
    global default_funcs

    if not default_funcs.get('log_report'):
        default_funcs['log_report'] = _pytest.terminal.TerminalReporter.pytest_runtest_logreport


def _report_on_terminal(self, report):
    def wrapper():
        return pytest_spec2md.spec_creator.create_specification_document(self, report, default_func=default_funcs['log_report'])

    return wrapper()


def pytest_configure(config):
    _initialize()
    import six

    if config.option.spec2md:
        pytest_spec2md.spec_creator.delete_existing_specification_file(config)

        config.addinivalue_line(
            "markers", "spec_reference(name, docstring): mark specification reference for the test"
        )

        _pytest.terminal.TerminalReporter.pytest_runtest_logreport = _report_on_terminal

    else:
        _pytest.terminal.TerminalReporter.pytest_runtest_logreport = default_funcs['log_report']

    six.moves.reload_module(_pytest)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Adds docstring to the item usage in report"""
    outcome = yield
    report = outcome.get_result()
    node = getattr(item, 'obj', None)
    if node:
        report.node = node
        report.node_parents = []
        parent = get_parent(node)
        while parent:
            report.node_parents.append(parent)
            parent = get_parent(parent)
        report.node_parents.reverse()

        report.reference_docs = []
        for marker in item.iter_markers_with_node(name='spec_reference'):
            report.reference_docs.append((marker[0], marker[1].args))


def get_parent(obj):
    try:
        parents = obj.__qualname__.split(".")
        if len(parents) > 1 and "<locals>" not in parents:
            full_name = obj.__module__ + "." + ".".join(parents[:-1])
            script = \
                f'exec("import {obj.__module__}") or {full_name}'
            x = eval(script, globals(), locals())
            return x

    except Exception as err:
        print(err)

    return None


def _get_parent_doc(function):
    func = getattr(function, "__self__", None)
    if not func:
        return ""
    parent = getattr(func, "__class__", None)
    if not parent:
        return ""

    doc = inspect.getdoc(parent)
    return doc if doc is not None else ""
