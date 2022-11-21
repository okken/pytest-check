"""
A test file with both `check` and `assert`, both failing
"""
from pytest_check import check


def test_fail_check():
    check.equal(1, 2)


def test_fail_assert():
    assert 1 == 2
