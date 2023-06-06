def test_failing_threaded_testcode(pytester):
    pytester.copy_example("examples/test_example_fail_in_thread.py")
    result = pytester.runpytest()
    result.assert_outcomes(failed=2, passed=0)
    result.stdout.fnmatch_lines(["*1 + 1 is 2, not 3*"])
    result.stdout.fnmatch_lines(["*1 + 1 is 2, not 4*"])


def test_passing_threaded_testcode(pytester):
    pytester.copy_example("examples/test_example_pass_in_thread.py")
    result = pytester.runpytest()
    result.assert_outcomes(failed=0, passed=2)
