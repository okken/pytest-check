def test_passing_check_helper_functions(pytester):
    pytester.copy_example("examples/test_example_check_func_decorator.py")
    result = pytester.runpytest("-k", "test_pass")
    result.assert_outcomes(passed=2)


def test_failing_check_helper_functions(pytester):
    pytester.copy_example("examples/test_example_check_func_decorator.py")
    result = pytester.runpytest("-s", "-k", "test_all_four")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*should_be_True=True*",
            "*should_be_False=False*",
            "*FAILURE: assert 1 == 4*",
            "*FAILURE: assert 2 == 4*",
            "*FAILURE: assert 3 == 4*",
            "*Failed Checks: 3*",
        ]
    )
