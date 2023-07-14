"""
helper1() should not be included in traceback
"""

from pytest_check import check


def test_func():
    helper1()


def helper1():
    __tracebackhide__ = True
    helper2()


def helper2():
    with check("first"):
        assert 1 == 0
    with check("second"):
        assert 1 > 2
