from pytest_check.context_manager import CheckContextManager


def test_something(check: CheckContextManager) -> None:
    check.equal(1, 2, "oops")
