import pytest_check as check

def test_failures():
    assert 0 == 0
    check.equal(1, 1)
    check.equal(0, 1)
    assert 1 == 2
    check.equal(2, 3)