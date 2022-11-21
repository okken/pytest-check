"""
Just a simple test to show passing and failing checks.
"""
from pytest_check import check


def test_pass():
    with check:
        assert 1 == 1


def test_fail():
    with check:
        assert 1 == 2
