# -*- coding: utf-8 -*-

import pytest
from .check import get_failures, clear_failures, set_stop_on_fail


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    evalxfail = getattr(item, "_evalxfail", None)
    failures = get_failures()
    clear_failures()

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
    set_stop_on_fail(config.getoption("-x"))
