"""
A test file with both `check` and `assert`, both failing
"""
from pytest_check import check
import logging

log = logging.getLogger(__name__)


def test_logging_error_level(caplog):
    log.warning("First check")
    check.equal("one", "xxx")
    log.warning("Second check")
    check.equal("two", "yyy")

    assert len(caplog.record_tuples) == 4
    assert caplog.record_tuples[0] == (
        'test_example_logging', logging.WARNING, 'First check'
    )
    assert caplog.record_tuples[1] == (
        'pytest_check.check_log',
        logging.ERROR,
        'FAILURE: check one == xxx\ntest_example_logging.py:12 '
        'in test_logging_error_level() -> check.equal("one", "xxx")\n'
    )
    assert caplog.record_tuples[2] == (
        'test_example_logging', logging.WARNING, 'Second check'
    )
    assert caplog.record_tuples[3] == (
        'pytest_check.check_log',
        logging.ERROR,
        'FAILURE: check two == yyy\ntest_example_logging.py:14 '
        'in test_logging_error_level() -> check.equal("two", "yyy")\n'
    )


def test_logging_no_level(caplog):
    log.warning("First check")
    check.equal("one", "xxx")
    log.warning("Second check")
    check.equal("two", "yyy")

    assert len(caplog.record_tuples) == 2
    assert caplog.record_tuples[0] == (
        'test_example_logging', logging.WARNING, 'First check'
    )
    assert caplog.record_tuples[1] == (
        'test_example_logging', logging.WARNING, 'Second check'
    )
