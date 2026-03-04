import pytest
from pytest_check import check


@pytest.mark.xfail(reason="None cannot be compared")
def test_none_less() -> None:
    check.less(None, 1)


@pytest.mark.xfail(reason="None cannot be compared")
def test_none_less_equal() -> None:
    check.less_equal(None, 1)


@pytest.mark.xfail(reason="None cannot be compared")
def test_none_greater() -> None:
    check.greater(1, None)


@pytest.mark.xfail(reason="None cannot be compared")
def test_none_greater_equal() -> None:
    check.greater_equal(1, None)


@pytest.mark.xfail(reason="None cannot be compared")
def test_none_between() -> None:
    check.between(1, None, 2)
