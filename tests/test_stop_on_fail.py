def test_stop_on_fail(pytester):
    pytester.copy_example("examples/test_example_stop_on_fail.py")
    result = pytester.runpytest("-x")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*> * check.equal(1, 2)*"])


def test_context_manager_stop_on_fail(pytester):
    pytester.copy_example("examples/test_example_context_manager_fail.py")
    result = pytester.runpytest("-x", "-k", "test_3_failed_checks")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(["*assert 1 == 0*"])


def test_context_manager_stop_on_fail_with_msg(pytester):
    pytester.copy_example("examples/test_example_context_manager_fail.py")
    result = pytester.runpytest("-x", "-k", "test_messages")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(["*first fail*"])
    result.stdout.no_fnmatch_line("*second fail*")
    result.stdout.no_fnmatch_line("*third fail*")
