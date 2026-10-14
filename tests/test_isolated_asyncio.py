from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from _pytest.pytester import Pytester


def test_isolated_asyncio(run_example_test: Callable) -> None:
    result = run_example_test("test_example_isolated_asyncio.py")
    result.assert_outcomes(failed=1)


def test_isolated_asyncio_in_subprocess(pytester: "Pytester") -> None:
    pytester.copy_example("examples/test_example_isolated_asyncio.py")
    result = pytester.runpytest_subprocess()
    result.assert_outcomes(failed=1)
