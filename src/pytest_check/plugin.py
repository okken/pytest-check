# -*- coding: utf-8 -*-

import pytest
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


def pytest_configure(config):
    check_methods.set_stop_on_fail(config.getoption("-x"))


@pytest.fixture(name='check')
def check_fixture():
    return check_methods
