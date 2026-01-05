from typing import Callable


# Number of test functions in test_example_functions_pass.py and test_example_functions_fail.py
NUM_CHECK_FUNCTION_TESTS = 25


def test_passing_check_functions(run_example_test: Callable) -> None:
    result = run_example_test("test_example_functions_pass.py")
    result.assert_outcomes(failed=0, passed=NUM_CHECK_FUNCTION_TESTS)
    # Verify that no failures were reported
    result.stdout.no_fnmatch_line("*FAILURE*")
    result.stdout.no_fnmatch_line("*Failed Checks*")


def test_failing_check_functions(run_example_test: Callable) -> None:
    result = run_example_test("test_example_functions_fail.py")
    result.assert_outcomes(failed=NUM_CHECK_FUNCTION_TESTS, passed=0)
    # Verify that failures were reported for each test
    failure_count = str(result.stdout).count("FAILURE:")
    assert failure_count >= NUM_CHECK_FUNCTION_TESTS, (
        f"Expected at least {NUM_CHECK_FUNCTION_TESTS} failures, "
        f"but found {failure_count}"
    )
    # Verify that all tests show "Failed Checks:" (some tests may have multiple checks)
    # Count all "Failed Checks:" lines to ensure all tests failed
    failed_checks_lines = str(result.stdout).count("Failed Checks:")
    assert failed_checks_lines == NUM_CHECK_FUNCTION_TESTS, (
        f"Expected {NUM_CHECK_FUNCTION_TESTS} 'Failed Checks:' lines (one per test), "
        f"but found {failed_checks_lines}"
    )
