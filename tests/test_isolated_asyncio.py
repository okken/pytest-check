from typing import Callable


def test_isolated_asyncio(run_example_test: Callable) -> None:
    result = run_example_test("test_example_isolated_asyncio.py")
    result.assert_outcomes(failed=1)