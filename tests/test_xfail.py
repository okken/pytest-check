
def test_xfail(pytester):
    pytester.copy_example("examples/test_example_xfail.py")
    result = pytester.runpytest("test_example_xfail.py::test_xfail")
    result.assert_outcomes(xfailed=1)
    result.stdout.fnmatch_lines(["* 1 xfailed *"])


def test_xfail_strict(pytester):
    pytester.copy_example("examples/test_example_xfail.py")
    result = pytester.runpytest("test_example_xfail.py::test_xfail_strict")
    result.assert_outcomes(xfailed=1)
    result.stdout.fnmatch_lines(["* 1 xfailed *"])


def test_xpass(pytester):
    pytester.copy_example("examples/test_example_xfail.py")
    result = pytester.runpytest("test_example_xfail.py::test_xfail_pass")
    result.assert_outcomes(xpassed=1)
    result.stdout.fnmatch_lines(["* 1 xpassed *"])


def test_xpass_strict(pytester):
    pytester.copy_example("examples/test_example_xfail.py")
    result = pytester.runpytest("test_example_xfail.py::test_xfail_pass_strict")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["* 1 failed *"])


def test_xfail_runxfail(pytester):
    pytester.copy_example("examples/test_example_xfail.py")
    result = pytester.runpytest("--runxfail", "test_example_xfail.py")
    result.assert_outcomes(passed=2, failed=9)
    result.stdout.fnmatch_lines(["* 9 failed, 2 passed *"])


def test_xfail_raises_should_fail_check(pytester):
    """Test that xfail with raises should fail when wrong exception type in check"""
    pytester.copy_example("examples/test_example_xfail.py")
    result = pytester.runpytest(
        "test_example_xfail.py::test_xfail_raises_should_fail_check"
    )
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["* 1 failed *"])


def test_xfail_raises_check_multiple_unmatched_marks(pytester):
    """Test that xfail with multiple unmatched raises should fail"""
    pytester.copy_example("examples/test_example_xfail.py")
    result = pytester.runpytest(
        "test_example_xfail.py::test_xfail_raises_check_multiple_unmatched_marks"
    )
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["* 1 failed *"])


def test_xfail_raises_should_fail_check_tuple_single_value(pytester):
    """Test that xfail with tuple of single unmatched exception should fail"""
    pytester.copy_example("examples/test_example_xfail.py")
    result = pytester.runpytest(
        "test_example_xfail.py::test_xfail_raises_should_fail_check_tuple_single_value"
    )
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["* 1 failed *"])


def test_xfail_no_raises_with_check(pytester):
    """Test backward compatibility: xfail without raises should still work with checks"""
    pytester.copy_example("examples/test_example_xfail.py")
    result = pytester.runpytest(
        "test_example_xfail.py::test_xfail_no_raises_with_check"
    )
    result.assert_outcomes(xfailed=1)
    result.stdout.fnmatch_lines(["* 1 xfailed *"])


def test_xfail_raises_assertion_error_matches(pytester):
    """Test that xfail works when the expected exception matches"""
    pytester.copy_example("examples/test_example_xfail.py")
    result = pytester.runpytest(
        "test_example_xfail.py::test_xfail_raises_assertion_error_matches"
    )
    result.assert_outcomes(xfailed=1)
    result.stdout.fnmatch_lines(["* 1 xfailed *"])


def test_xfail_raises_tuple_matches(pytester):
    """Test that xfail works when one exception in tuple matches"""
    pytester.copy_example("examples/test_example_xfail.py")
    result = pytester.runpytest(
        "test_example_xfail.py::test_xfail_raises_tuple_matches"
    )
    result.assert_outcomes(xfailed=1)
    result.stdout.fnmatch_lines(["* 1 xfailed *"])


def test_xfail_raises_multiple_marks_one_matches(pytester):
    """Test that xfail works when one of multiple marks matches"""
    pytester.copy_example("examples/test_example_xfail.py")
    result = pytester.runpytest(
        "test_example_xfail.py::test_xfail_raises_multiple_marks_one_matches"
    )
    result.assert_outcomes(xfailed=1)
    result.stdout.fnmatch_lines(["* 1 xfailed *"])
