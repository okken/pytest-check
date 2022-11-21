from pytest_check import raises
from pytest_check import check


def test_raises_top_level_fail():
    with raises(AssertionError):
        x = 3
        assert 1 < x < 4


def test_raises_top_level_pass():
    with raises(AssertionError):
        x = 4
        assert 1 < x < 3


def test_raises_check_level_fail():
    with check.raises(AssertionError):
        x = 3
        assert 1 < x < 4


def test_raises_check_level_pass():
    with check.raises(AssertionError):
        x = 4
        assert 1 < x < 3
