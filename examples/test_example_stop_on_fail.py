"""
An example useful for playing with stop on fail.

-x or --maxfail=1 should result in one failed check and one failed test.

--maxfail=2 should run both tests and catch all 4 check failures

This is because --maxfail=1/-x stops on first failure, check or assert.
Using --maxfail=2 or more counts failing test functions, not check failures.
"""

from pytest_check import check


class TestStopOnFail:
    def test_1(self):
        check.equal(1, 1)
        check.equal(1, 2)
        check.equal(1, 3)

    def test_2(self):
        check.equal(1, 1)
        check.equal(1, 2)
        check.equal(1, 3)
