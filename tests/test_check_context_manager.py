def test_context_manager_pass(pytester):
    pytester.copy_example("examples/test_example_context_manager_pass.py")
    result = pytester.runpytest()
    result.assert_outcomes(passed=2)


def test_context_manager_fail(pytester):
    pytester.copy_example("examples/test_example_context_manager_fail.py")
    result = pytester.runpytest("-k", "test_3_failed_checks")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: assert 1 == 0*",
            "*FAILURE: assert 1 > 2*",
            "*FAILURE: assert 5 < 4*",
            "*Failed Checks: 3*",
        ]
    )


def test_context_manager_fail_with_msg(pytester):
    pytester.copy_example("examples/test_example_context_manager_fail.py")
    result = pytester.runpytest("-k", "test_messages")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: first fail*",
            "*FAILURE: second fail*",
            "*FAILURE: third fail*",
            "*Failed Checks: 3*",
        ]
    )
