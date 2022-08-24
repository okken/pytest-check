def test_check_not_in_a_test(pytester):
    """
    should error
    """
    pytester.copy_example("examples/test_example_check_not_in_test.py")
    result = pytester.runpytest()
    result.assert_outcomes(errors=1, failed=0, passed=0)
    result.stdout.fnmatch_lines([
        "* ERROR at setup of test_something *",
        "*FAILURE: assert 1 == 0*",
        "*not_in_test.py:* in not_in_a_test() -> helper_func()*",
        "*not_in_test.py:* in helper_func() -> with check:*",
        "*Failed Checks: 1*",
        "* short test summary info *",
        "*ERROR test_example_check_not_in_test.py::test_something*",
    ])
