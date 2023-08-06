import datetime
import importlib
import os

import _pytest.reports


def modify_items_of_collection(session, config, items):
    """
    Sort the found tests for better results in output
    """
    _delete_existing_file(config.getini('spec_target_file'))

    def get_module_name(f):
        return f.listchain()[1].name

    def get_nodeid(f):
        return "::".join(f.nodeid.split('::')[:-1])

    items.sort(key=get_nodeid)
    items.sort(key=get_module_name)
    return items


def _delete_existing_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def create_logreport(self, report: _pytest.reports.TestReport, use_terminal=True):
    filename = self.config.getini('spec_target_file')
    _create_spec_file_if_not_exists(os.path.join(os.getcwd(), filename))
    if report.when == 'call':
        result, _, _ = self.config.hook.pytest_report_teststatus(report=report, config=self.config)
        self.stats.setdefault(result, []).append(report)

        _write_node_to_file(filename, _create_file_content(report, result))

        if use_terminal:
            print(f'{report.nodeid} {"." if report.passed else "F"}')


def _create_spec_file_if_not_exists(filename):
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w') as file:
            file.writelines([
                '# Specification\n',
                'Automatically generated using pytest_spec2md  \n'
                f'Generated: {datetime.datetime.now()}  \n'
                f'\n',
            ])


def _create_file_content(report, state):
    return report


def _split_scope(testnode):
    data = [i for i in testnode.split('::') if i != '()']
    if data[-1].endswith("]"):
        data[-1] = data[-1].split("[")[0]
    return data


_last_parents: list = []
_last_node_content: _pytest.reports.TestReport = None


def _format_test_name(name: str):
    if name is not str:
        name = str(name)
    if name.endswith("["):
        name = name[:name.find("[")]
    return name.replace('test_', '', 1).replace('_', ' ')


def _format_class_name(name: str):
    if name is not str:
        name = str(name.__name__)
    name = name.replace('Test', '', 1)
    return ''.join(' ' + x if x.isupper() else x for x in name)


def format_doc_string(doc_string: str):
    if not doc_string:
        return []
    return [x.strip() for x in doc_string.split("\n") if x.strip()]


def _write_node_to_file(filename, node_content: _pytest.reports.TestReport):
    global _last_parents
    global _last_node_content

    if not os.path.exists(filename):
        raise ValueError(f'File not found: {filename}')

    parents = getattr(node_content, "node_parents", [])

    last_module = _split_scope(_last_node_content.nodeid)[0] if _last_node_content else ""
    act_module = _split_scope(node_content.nodeid)[0]

    last_tc_name = _split_scope(_last_node_content.nodeid)[-1] if _last_node_content else ""
    act_tc_name = _split_scope(node_content.nodeid)[-1]

    longnewline = "  \n  "
    shortnewline = "\n"
    print_testcase = False

    with open(filename, 'a') as file:
        if not last_module or last_module != act_module:  # changed test file
            write_module_info_to_file(act_module, file)

        if len(parents) == 0:
            if last_module != act_module:
                file.write(
                    f'\n'
                    f'### General\n'
                    f'\n'
                )
                print_testcase = True
        else:
            show_recursive = False
            line_start = '###'
            last_parents = _last_parents.copy()
            last_parents.extend(["" for _ in range(len(parents) - len(last_parents))])
            for act, last in zip(parents, last_parents):
                if show_recursive or act != last:
                    show_recursive = True
                    doc_lines = format_doc_string(getattr(act, "__doc__"))
                    file.write(
                        f'\n'
                        f'{line_start}{_format_class_name(act)}\n' +
                        (f'  {shortnewline.join(doc_lines)}  \n' if doc_lines else '')
                    )
                    write_references(node_content, act, file)
                    file.write(f'\n')

                    print_testcase = True
                line_start += '#'

        if print_testcase or act_tc_name != last_tc_name:
            tc = getattr(node_content, "node", None)
            doc_lines = format_doc_string(getattr(tc, "__doc__"))

            file.write(
                f' - **{_format_test_name(act_tc_name)}**  \n' +
                (f'  {longnewline.join(doc_lines)}\n' if doc_lines else '')
            )
            write_references(node_content, tc, file)

    _last_parents = parents
    _last_node_content = node_content


def write_module_info_to_file(act_module, file):
    module_name = act_module.replace('/', '.')[:-3]
    mod = importlib.import_module(module_name)
    doc_lines = format_doc_string(mod.__doc__)
    shortnewline = "\n"

    file.write(
        f'## Spec from {act_module}\n' +
        (f'{shortnewline.join(doc_lines)}  \n' if doc_lines else '')
    )


def write_references(node_content, act_obj, file):
    longnewline = "  \n  "
    references = getattr(node_content, "reference_docs", [])
    for target, reference in references:
        if target.obj == act_obj:
            file.write(
                (f'  Tests: *{reference[0]}*  \n' if reference[0] else '') +
                (f'  {longnewline.join(format_doc_string(reference[1]))}\n' if len(reference) > 1 else '')
            )
