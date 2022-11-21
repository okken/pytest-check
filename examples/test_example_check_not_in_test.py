"""
The `check` context manager is intended to be used by tests
and helper functions.
But we need to make sure it doesn't blow up if called elsewhere.

This test file should result in an error test result.
"""

from pytest_check import check


def not_in_a_test():
    helper_func()


def helper_func():
    with check:
        assert 1 == 0


# called at import time.
# not a good practice
# but should result in a test error report
not_in_a_test()


def test_something():
    pass
