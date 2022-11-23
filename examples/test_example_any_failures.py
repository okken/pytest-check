"""
Stop checking if any failure in first block of checks.

It's not worth second block of checks if any failure in the first block

"""
from pytest_check import check
from pytest_check import any_failures


def test_any_failures_false():
    check.equal(1, 1)
    check.equal(2, 2)
    if not any_failures():
        check.equal(1, 2)
        check.equal(1, 3)
        check.equal(1, 4)


def test_any_failures_true():
    check.equal(1, 1)
    check.equal(2, 3)
    if not any_failures():
        check.equal(1, 2)
        check.equal(2, 2)
        check.equal(1, 3)
        check.equal(1, 4)
        check.equal(1, 5)
