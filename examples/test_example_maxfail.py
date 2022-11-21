"""
Running: pytest --maxfail=1 test_example_maxfail.py
Should cause pytest to stop after the first failed check in test_a

Running: pytest --maxfail=2 test_example_maxfail.py
Should run a and b, but not c

Running: pytest --maxfail=3 test_example_maxfail.py
Should run a, b, and c

This is because pytest-check has a special case for maxfail==1.
If maxfail==1, stop on the first failed check.
If > 1, run until 2 failed "tests", not "checks".
"""

from pytest_check import check


def test_a():
    "failing test: 3 failed checks"
    with check:
        assert False, "one"
    with check:
        assert False, "two"
    with check:
        assert False, "three"


def test_b():
    "failing test"
    assert False


def test_c():
    "passing test"
    assert True
