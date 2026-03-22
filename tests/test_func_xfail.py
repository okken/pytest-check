def test_xfail(pytester):
    pytester.copy_example("examples/test_example_check_func_xfail.py")
    result = pytester.runpytest("-k", "test_should_xfail")
    result.assert_outcomes(xfailed=2, failed=0, passed=0, xpassed=0)

def test_xpass(pytester):
    pytester.copy_example("examples/test_example_check_func_xfail.py")
    result = pytester.runpytest("-k", "test_should_xpass")
    result.assert_outcomes(xfailed=0, failed=0, passed=0, xpassed=1)

def test_pass(pytester):
    pytester.copy_example("examples/test_example_check_func_xfail.py")
    result = pytester.runpytest("-k", "test_should_pass")
    result.assert_outcomes(xfailed=0, failed=0, passed=1, xpassed=0)

def test_fail(pytester):
    pytester.copy_example("examples/test_example_check_func_xfail.py")
    result = pytester.runpytest("-k", "test_should_fail")
    result.assert_outcomes(xfailed=0, failed=2, passed=0, xpassed=0)