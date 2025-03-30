def test_skip_teardown_fail(pytester):
    pytester.copy_example("examples/test_example_fail_in_teardown_with_skip.py")
    result = pytester.runpytest()
    result.assert_outcomes(passed=1, skipped=1, errors=1)
