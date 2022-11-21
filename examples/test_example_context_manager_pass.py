"""
Context manater with one or multiple blocks.
"""
from pytest_check import check


def test_one_with_block():
    with check:
        x = 3
        assert 1 < x < 4


def test_multiple_with_blocks():
    x = 3
    with check:
        assert 1 < x
    with check:
        assert x < 4
    with check:
        assert x == 3
