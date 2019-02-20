# -*- coding: utf-8 -*-

import pytest
from . import check


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    evalxfail = getattr(item, "_evalxfail", None)
    failures = check.get_failures()
    check.clear_failures()

    if call.when == "call" and failures:
        if evalxfail and evalxfail.wasvalid() and evalxfail.istrue():
            report.outcome = "skipped"
            report.wasxfail = evalxfail.getexplanation()
        else:
            summary = "Failed Checks: {}".format(len(failures))
            longrepr = ["\n".join(failures)]
            longrepr.append("-" * 60)
            longrepr.append(summary)
            report.longrepr = "\n".join(longrepr)
            report.outcome = "failed"


def pytest_configure(config):
    check.set_stop_on_fail(config.getoption("-x"))


@pytest.fixture(name='check')
def check_fixture():
    return check
