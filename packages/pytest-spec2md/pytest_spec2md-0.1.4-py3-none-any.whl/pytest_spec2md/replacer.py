from . import patch


def logstart(self, nodeid, location):
    def wrapper():
        def inner_function(self, nodeid, location):
            """
            Signal the start of running a single test item.
            """
            #  Hook has to be disabled to prevent additional information
            pass

        return inner_function(self, nodeid, location)

    return wrapper()


def report_on_terminal(self, report):
    def wrapper():
        return patch.create_logreport(self, report, use_terminal=True)

    return wrapper()


def report_no_terminal(self, report):
    def wrapper():
        return patch.create_logreport(self, report, use_terminal=False)

    return wrapper()


def modify_items(session, config, items):
    def wrapper():
        return patch.modify_items_of_collection(session, config, items)

    return wrapper()
