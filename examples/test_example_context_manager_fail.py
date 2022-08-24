"""
should have 3 failed checks, all reported.
should have one failed test
"""

from pytest_check import check

def test_failures():
    with check: assert 1 == 0
    with check: assert 1 > 2
    with check: assert 1 < 5 < 4