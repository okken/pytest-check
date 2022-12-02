from pytest_check import check
from pytest_check import any_failures


def test_any_failures_false(pytester):
    pytester.copy_example("examples/test_example_any_failures.py")
    result = pytester.runpytest("-k", "test_any_failures_false")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*check 1 == 2*",
            "*check 1 == 3*",
            "*check 1 == 4*",
            "*Failed Checks: 3",
        ]
    )


def test_any_failure_true(pytester):
    pytester.copy_example("examples/test_example_any_failures.py")
    result = pytester.runpytest("-k", "test_any_failures_true")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*check 2 == 3*",
            "*Failed Checks: 1",
        ]
    )


def test_top_level():
    assert not any_failures()


def test_from_imported_check():
    assert not check.any_failures()


def test_from_check_fixture(check):
    assert not check.any_failures()
