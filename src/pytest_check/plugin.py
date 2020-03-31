# -*- coding: utf-8 -*-

import pytest
from . import check_methods


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
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


CONFIG = None


def pytest_configure(config):
    global CONFIG
    check_methods.set_stop_on_fail(config.getoption("-x"))
    CONFIG = config


@pytest.fixture(name='check')
def check_fixture():
    return check_methods
