"""
Make sure locals can be viewed with -l or --showlocals
"""

from pytest_check import check


def test_ctx():
    a = 1
    with check:
        b = 2
        assert a == b

def test_check_func():
    a = 1
    b = 2
    check.equal(a, b)
