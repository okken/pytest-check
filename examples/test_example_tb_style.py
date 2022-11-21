"""
Useful for making sure `tb=no` turns off pseudo-traceback.
"""
from pytest_check import check


def run_helper2():
    with check("first fail"):
        assert 1 == 0
    with check("second fail"):
        assert 1 > 2
    with check("third fail"):
        assert 1 < 5 < 4


def run_helper1():
    run_helper2()


def test_failures():
    run_helper1()
