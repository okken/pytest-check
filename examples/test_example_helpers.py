"""
Make sure checks can be run in helper functions
and that a walk though of functions from test_something()
to the point of failure is reported.
"""

from pytest_check import check


def test_func():
    helper1()


def helper1():
    helper2()


def helper2():
    with check("first"):
        assert 1 == 0
    with check("second"):
        assert 1 > 2
