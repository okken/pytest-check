"""
Mixing assertions and checks can be confusing.

With normal test run, a failing assertion should take precedence over
a failing check.

With -x/--maxfail=1, the first failed check or assertion should
stop the test.
"""

from pytest_check import check


def test_failures():
    assert 0 == 0
    check.equal(1, 1)
    check.equal(0, 1)  # failure
    assert 1 == 2  # failure
    check.equal(2, 3)  # failure
