"""
It is no longer recommended to do this:

    import pytest_check

    def test_old_style():
        pytest_check.equal(1, 1)

or this:

    import pytest_check as check

    def test_old_style():
        check.equal(1, 1)

However, it used to work.
It still works.
But this method is deprecated and may be removed in future versions.

Please migrate to this:

    from pytest_check import check

    def test_pass():
        check.equal(1, 1)
"""
from pytest_check import check
import pytest_check


def test_old_style():
    pytest_check.equal(1, 1)


def test_pass():
    check.equal(1, 1)
    with check:
        assert 1 == 1


def test_pass_check(check):
    check.equal(1, 1)
    with check:
        assert 1 == 1
