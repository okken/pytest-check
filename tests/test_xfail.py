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
