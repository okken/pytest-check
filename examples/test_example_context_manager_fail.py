"""
Everything should fail in this file.
This test is useful for testing:
-  messages
- stop on fail (-x)
- pseudo-tracebacks
- lack of tracebacks (--tb=no)
"""

from pytest_check import check


def test_3_failed_checks():
    with check:
        assert 1 == 0
    with check:
        assert 1 > 2
    with check:
        assert 1 < 5 < 4


def test_messages():
    with check("first fail"):
        assert 1 == 0
    with check("second fail"):
        assert 1 > 2
    with check("third fail"):
        assert 1 < 5 < 4
