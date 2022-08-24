def test_maxfail_1_stops_on_first_check(pytester):
    """
    Should stop after first failed check
    """
    pytester.copy_example("examples/test_example_maxfail.py")
    result = pytester.runpytest("--maxfail=1")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(["*AssertionError: one*"])


def test_maxfail_2_stops_on_two_failed_tests(pytester):
    """
    Should stop after 2 tests (not checks)
    """
    pytester.copy_example("examples/test_example_maxfail.py")
    result = pytester.runpytest("--maxfail=2")
    result.assert_outcomes(failed=2, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: one",
            "*FAILURE: two",
            "*FAILURE: three",
            "*Failed Checks: 3*",
        ]
    )


def test_maxfail_3_runs_at_least_3_tests(pytester):
    """
    Should not stop on checks.
    """
    pytester.copy_example("examples/test_example_maxfail.py")
    result = pytester.runpytest("--maxfail=3")
    result.assert_outcomes(failed=2, passed=1)
