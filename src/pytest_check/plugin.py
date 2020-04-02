# -*- coding: utf-8 -*-

import pytest
from . import check_methods

# Note. the evalxfail gymnastics are ugly, no doubt
# This is to get around pytest not providing a good
# public way to get at xfail behavior.
# The current state is working as of pytest 5.4.1
# thanks to Anthony Sottile for the workaround.

try:
    from _pytest.skipping import evalxfail_key
except ImportError:
    evalxfail_key = None


_current_item = None


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if evalxfail_key is not None:
        try:
            evalxfail = item._store[evalxfail_key]
        except KeyError:
            evalxfail = None
    else:
        evalxfail = getattr(item, "_evalxfail", None)

    failures = check_methods.get_failures()
    check_methods.clear_failures()

    if failures:
        if evalxfail and evalxfail.wasvalid() and evalxfail.istrue():
            report.outcome = "skipped"
            report.wasxfail = evalxfail.getexplanation()
        elif outcome._result.longreprtext.startswith("[XPASS(strict)]"):
            report.outcome = "skipped"
            report.wasxfail = "\n".join(failures)
        else:
            summary = "Failed Checks: {}".format(len(failures))
            longrepr = ["\n".join(failures)]
            longrepr.append("-" * 60)
            longrepr.append(summary)
            report.longrepr = "\n".join(longrepr)
            report.outcome = "failed"


def pytest_addhooks(pluginmanager):
    from . import hooks
    pluginmanager.add_hookspecs(hooks)


def pytest_configure(config):
    check_methods.set_stop_on_fail(config.getoption("-x"))


def pytest_runtest_setup(item):
    global _current_item
    _current_item = item


def pytest_runtest_call(item):
    global _current_item
    _current_item = item


def pytest_runtest_teardown(item):
    global _current_item
    _current_item = item


def fire_pass_hook():
    _current_item.config.hook.pytest_check_pass(item=_current_item)


def fire_fail_hook(exception):
    _current_item.config.hook.pytest_check_fail(exception=exception,
                                                item=_current_item)


@pytest.fixture(name='check')
def check_fixture():
    return check_methods
