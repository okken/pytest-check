from typing import Callable


def test_stop_on_fail(run_example_test: Callable) -> None:
    result = run_example_test("test_example_stop_on_fail.py", None, "-x")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["> * check.equal(1, 2)*"])


def test_context_manager_stop_on_fail(run_example_test: Callable) -> None:
    result = run_example_test(
        "test_example_context_manager_fail.py", "test_3_failed_checks", "-x"
    )
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(["*assert 1 == 0*"])


def test_context_manager_stop_on_fail_with_msg(run_example_test: Callable) -> None:
    result = run_example_test(
        "test_example_context_manager_fail.py", "test_messages", "-x"
    )
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(["*first fail*"])
    result.stdout.no_fnmatch_line("*second fail*")
    result.stdout.no_fnmatch_line("*third fail*")
