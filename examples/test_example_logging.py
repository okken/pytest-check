"""
A test file to try with without logging-level option
"""
from pytest_check import check
import logging

log = logging.getLogger(__name__)


def test_error_level(caplog):
    log.warning("First check")
    check.equal("one", "xxx")
    log.warning("Second check")
    check.equal("two", "yyy")

    assert len(caplog.record_tuples) == 4

    message = caplog.record_tuples[0][2]
    assert message == 'First check'

    _, level, message = caplog.record_tuples[1]
    assert level == logging.ERROR
    assert 'FAILURE: check one' in message

    message = caplog.record_tuples[2][2]
    assert message == 'Second check'

    _, level, message = caplog.record_tuples[3]
    assert level == logging.ERROR
    assert 'FAILURE: check two' in message


def test_no_level(caplog):
    log.warning("First check")
    check.equal("one", "xxx")
    log.warning("Second check")
    check.equal("two", "yyy")

    assert len(caplog.record_tuples) == 2

    message = caplog.record_tuples[0][2]
    assert message == 'First check'

    message = caplog.record_tuples[1][2]
    assert message == 'Second check'
