def test_check_and_assert(pytester):
    pytester.copy_example("examples/test_example_check_and_assert.py")
    result = pytester.runpytest()
    result.assert_outcomes(failed=2)
    result.stdout.fnmatch_lines(["* 2 failed *"])
