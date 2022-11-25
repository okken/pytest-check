"""
`any_failures()` can be used to determine if more checks are needed.
"""
from pytest_check import check


def test_any_failures_false():
    check.equal(1, 1)
    check.equal(2, 2)
    if not check.any_failures():
        check.equal(1, 2)
        check.equal(1, 3)
        check.equal(1, 4)


def test_any_failures_true():
    check.equal(1, 1)
    check.equal(2, 3)
    if not check.any_failures():
        check.equal(1, 2)
        check.equal(2, 2)
        check.equal(1, 3)
        check.equal(1, 4)
        check.equal(1, 5)
