import sys
import os

import pytest
from _pytest._code.code import ExceptionInfo
from _pytest.skipping import xfailed_key
from _pytest.reports import ExceptionChainRepr
from _pytest._code.code import ExceptionRepr, ReprFileLocation

from . import check_log, check_raises, context_manager, pseudo_traceback


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    num_failures = check_log._num_failures
    failures = check_log.get_failures()
    check_log.clear_failures()

    if failures:
        if item._store[xfailed_key]:
            report.outcome = "skipped"
            report.wasxfail = item._store[xfailed_key].reason
        else:

            summary = f"Failed Checks: {num_failures}"
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
            except AssertionError as e:
                excinfo = ExceptionInfo.from_current()
                if (pytest.version_tuple >= (7,3,0)
                        and not os.getenv('PYTEST_XDIST_WORKER')):
                    # Build a summary report with failure reason
                    # Depends on internals of pytest, which changed in 7.3
                    # Also, doesn't work with xdist
                    #
                    # Example: Before 7.3:
                    #   =========== short test summary info ===========
                    #   FAILED test_example_simple.py::test_fail
                    # Example after 7.3:
                    #   =========== short test summary info ===========
                    #   FAILED test_example_simple.py::test_fail - assert 1 == 2
                    #
                    e_str = str(e)
                    e_str = e_str.split('FAILURE: ')[1]  # Remove redundant "Failure: "
                    reprcrash = ReprFileLocation(item.nodeid, 0, e_str)
                    reprtraceback = ExceptionRepr(reprcrash, excinfo)
                    chain_repr = ExceptionChainRepr([(reprtraceback, reprcrash, str(e))])
                    report.longrepr = chain_repr
                else:  # pragma: no cover
                    # coverage is run on latest pytest
                    # we'll have one test run on an older pytest just to make sure
                    # it works.
                    ...

            call.excinfo = excinfo


def pytest_configure(config):
    # Add some red to the failure output, if stdout can accommodate it.
    isatty = sys.stdout.isatty()
    color = getattr(config.option, "color", None)
    check_log.should_use_color = (isatty and color == "auto") or (color == "yes")

    # If -x or --maxfail=1, then stop on the first failed check
    # Otherwise, let pytest stop on the maxfail-th test function failure
    maxfail = config.getvalue("maxfail")
    stop_on_fail = maxfail == 1

    # TODO: perhaps centralize where we're storing stop_on_fail
    context_manager._stop_on_fail = stop_on_fail
    check_raises._stop_on_fail = stop_on_fail
    check_log._stop_on_fail = stop_on_fail

    # Allow for --tb=no to turn off check's pseudo tbs
    traceback_style = config.getoption("tbstyle", default=None)
    pseudo_traceback._traceback_style = traceback_style
    check_log._showlocals = config.getoption("showlocals", default=None)

    # grab options
    check_log._default_max_fail = config.getoption("--check-max-fail")
    check_log._default_max_report = config.getoption("--check-max-report")
    check_log._default_max_tb = config.getoption("--check-max-tb")


# Allow for tests to grab "check" via fixture:
# def test_a(check):
#    check.equal(a, b)
@pytest.fixture(name="check")
def check_fixture():
    return context_manager.check


# add some options
def pytest_addoption(parser):
    parser.addoption(
        "--check-max-report",
        action="store",
        type=int,
        help="max failures to report",
    )
    parser.addoption(
        "--check-max-fail",
        action="store",
        type=int,
        help="max failures per test",
    )
    parser.addoption(
        "--check-max-tb",
        action="store",
        type=int,
        default=1,
        help="max pseudo-tracebacks per test",
    )
