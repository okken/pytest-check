def test_setup_failure(pytester):
    pytester.copy_example("examples/test_example_fail_in_fixture.py")
    result = pytester.runpytest("-k", "test_setup_failure")
    result.assert_outcomes(errors=1)
    result.stdout.fnmatch_lines(["* check.equal(1, 2)*"])


def test_teardown_failure(pytester):
    pytester.copy_example("examples/test_example_fail_in_fixture.py")
    result = pytester.runpytest("-k", "test_teardown_failure")
    result.assert_outcomes(passed=1, errors=1)
    result.stdout.fnmatch_lines(["* check.equal(1, 2)*"])
