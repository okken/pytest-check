from typing import TYPE_CHECKING, Any, Callable, Optional

import pytest

pytest_plugins = "pytester"

if TYPE_CHECKING:
    from _pytest.pytester import Pytester

# RunResult is not available in type stubs, use Any as return type
RunResult = Any


@pytest.fixture
def run_example_test(pytester: "Pytester") -> Callable[..., "RunResult"]:
    """
    Fixture that returns a helper function to run tests from examples directory.

    Usage:
        def test_something(run_example_test):
            result = run_example_test("test_example_simple.py")
            result.assert_outcomes(passed=1)

    Args:
        pytester: The pytester fixture (injected by pytest)

    Returns:
        A function that takes (example_name, test_filter=None, *pytest_args) and returns RunResult
    """

    def _run_example_test(
        example_name: str,
        test_filter: Optional[str] = None,
        *pytest_args: str,
    ) -> "RunResult":
        """
        Helper function to run tests from examples directory.

        Args:
            example_name: Name of the example file (e.g., "test_example_simple.py")
            test_filter: Optional test filter for -k option
            *pytest_args: Additional pytest arguments

        Returns:
            RunResult from pytest execution
        """
        pytester.copy_example(f"examples/{example_name}")
        args = list(pytest_args)
        if test_filter:
            args.extend(["-k", test_filter])
        return pytester.runpytest(*args)

    return _run_example_test
