# -*- coding: utf-8 -*-

import pytest
from _pytest._code.code import ExceptionInfo
from . import check_methods

# This is ugly.
# But it seems to be the only way to know about xfail status.
from _pytest.skipping import xfailed_key


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    failures = check_methods.get_failures()
    check_methods.clear_failures()

    if failures:
        if item._store[xfailed_key]:
            report.outcome = "skipped"
            report.wasxfail = item._store[xfailed_key].reason
        else:

            summary = "Failed Checks: {}".format(len(failures))
            longrepr = ["\n".join(failures)]
            longrepr.append("-" * 60)
            longrepr.append(summary)

            if report.longrepr:
                longrepr.append("-" * 60)
                longrepr.append(report.longreprtext)
                report.longrepr = "\n".join(longrepr)
            else:
                report.longrepr = "\n".join(longrepr)
            report.outcome = "failed"
            try:
                raise AssertionError(report.longrepr)
            except AssertionError:
                excinfo = ExceptionInfo.from_current()
            call.excinfo = excinfo


def pytest_configure(config):
    maxfail = config.getvalue("maxfail")
    stop_on_fail = maxfail == 1
    # If -x or --maxfail=1, then stop on the first failed check
    # Otherwise, let pytest stop on the maxfail-th test function failure
    check_methods.set_stop_on_fail(stop_on_fail)


@pytest.fixture(name="check")
def check_fixture():
    return check_methods
