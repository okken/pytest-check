from typing import Callable

from pytest_check import any_failures, check


def test_any_failures_returns_true_when_checks_fail(run_example_test: Callable) -> None:
    result = run_example_test("test_example_any_failures.py", "test_any_failures_false")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*check 1 == 2*",
            "*check 1 == 3*",
            "*check 1 == 4*",
            "*Failed Checks: 3",
        ],
    )


def test_any_failures_returns_true_when_single_check_fails(
    run_example_test: Callable,
) -> None:
    result = run_example_test("test_example_any_failures.py", "test_any_failures_true")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*check 2 == 3*",
            "*Failed Checks: 1",
        ],
    )


def test_top_level():
    assert not any_failures()


def test_from_imported_check():
    assert not check.any_failures()


def test_from_check_fixture(check):
    assert not check.any_failures()
