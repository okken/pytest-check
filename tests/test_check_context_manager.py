from typing import Callable


def test_context_manager_passes_when_assertions_pass(
    run_example_test: Callable,
) -> None:
    result = run_example_test("test_example_context_manager_pass.py")
    result.assert_outcomes(passed=2)
    # Verify no failures were reported
    result.stdout.no_fnmatch_line("*FAILURE*")
    result.stdout.no_fnmatch_line("*Failed Checks*")


def test_context_manager_collects_multiple_failures(run_example_test: Callable) -> None:
    result = run_example_test(
        "test_example_context_manager_fail.py", "test_3_failed_checks"
    )
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: assert 1 == 0*",
            "*FAILURE: assert 1 > 2*",
            "*FAILURE: assert 5 < 4*",
            "*Failed Checks: 3*",
        ],
    )
    # Verify that all three failures were reported
    failure_count = str(result.stdout).count("FAILURE:")
    assert (
        failure_count >= 3
    ), f"Expected at least 3 failures, but found {failure_count}"


def test_context_manager_shows_custom_messages_on_failure(
    run_example_test: Callable,
) -> None:
    result = run_example_test("test_example_context_manager_fail.py", "test_messages")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: assert 1 == 0, first fail*",
            "*FAILURE: assert 1 > 2, second fail*",
            "*FAILURE: assert 5 < 4, third fail*",
            "*Failed Checks: 3*",
        ],
    )
    # Verify that all custom messages were included
    assert "first fail" in str(result.stdout)
    assert "second fail" in str(result.stdout)
    assert "third fail" in str(result.stdout)
