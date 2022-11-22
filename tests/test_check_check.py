def test_check_check(pytester):
    pytester.copy_example("examples/test_example_check_check.py")
    result = pytester.runpytest()
    result.assert_outcomes(failed=0, passed=2)
