def test_passing_check_functions(pytester):
    pytester.copy_example("examples/test_example_functions_pass.py")
    result = pytester.runpytest()
    result.assert_outcomes(failed=0, passed=25)


def test_failing_check_functions(pytester):
    pytester.copy_example("examples/test_example_functions_fail.py")
    result = pytester.runpytest()
    result.assert_outcomes(failed=25, passed=0)
