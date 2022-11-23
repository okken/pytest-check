def test_any_failures_false(pytester):
    pytester.copy_example("examples/test_example_any_failures.py")
    result = pytester.runpytest("-k", "test_any_failures_false")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*assert 1 == 2*",
            "*assert 1 == 3*",
            "*assert 1 == 4*",
            "*Failed Checks: 3",
        ]
    )


def test_any_failure_true(pytester):
    pytester.copy_example("examples/test_example_any_failures.py")
    result = pytester.runpytest("-k", "test_any_failures_true")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*assert 2 == 3*",
            "*Failed Checks: 1",
        ]
    )
