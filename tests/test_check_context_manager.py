from pytest import LineMatcher
from pytest_check import check

# properly formatted tests in
# multiline strings contain blank lines with spaces, freaks out flake8

# flake8: noqa


def test_context_manager():
    """
    passing check
    """
    with check:
        x = 3
        assert 1 < x < 4


def test_context_manager_with_msg():
    """
    check.msg only valid during with block
    really a unit test
    """
    with check("Hello"):
        assert check.msg == "Hello"
    assert check.msg is None


def test_context_manager_fail(pytester):
    pytester.copy_example("examples/test_example_context_manager_fail.py")
    result = pytester.runpytest()
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: assert 1 == 0*",
            "*FAILURE: assert 1 > 2*",
            "*FAILURE: assert 5 < 4*",
            "* assert 1 < 5 < 4*",
            "*Failed Checks: 3*",
        ]
    )


def test_context_manager_fail_with_msg(testdir):
    testdir.makepyfile(
        """
        from pytest_check import check

        def test_failures():
            with check("first fail"): assert 1 == 0
            with check("second fail"): assert 1 > 2
            with check("third fail"): assert 1 < 5 < 4
    """
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: first fail*",
            "*FAILURE: second fail*",
            "*FAILURE: third fail*",
            "* assert 1 < 5 < 4*",
            "*Failed Checks: 3*",
        ]
    )


def test_stop_on_fail(testdir):
    testdir.makepyfile(
        """
        from pytest_check import check

        def test_failures():
            with check: assert 1 == 0
            with check: assert 1 > 2
            with check: assert 1 < 5 < 4
    """
    )

    result = testdir.runpytest("-x")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(["*assert 1 == 0*"])


def test_stop_on_fail_with_msg(testdir):
    testdir.makepyfile(
        """
        from pytest_check import check

        def test_failures():
            with check("first fail"): assert 1 == 0
            with check("second fail"): assert 1 > 2
            with check("third fail"): assert 1 < 5 < 4
    """
    )

    result = testdir.runpytest("-x")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(["*first fail*"])


def test_traceback_style_no(testdir):
    testdir.makepyfile(
        """
        from pytest_check import check

        def run_helper1():
            with check("first fail"): assert 1 == 0
            with check("second fail"): assert 1 > 2
            with check("third fail"): assert 1 < 5 < 4

        def test_failures():
            run_helper1()
    """
    )

    result = testdir.runpytest("--junitxml=output.xml", "--tb=no")
    result.assert_outcomes(failed=1, passed=0)
    with open("output.xml") as f:
        lines = LineMatcher(f.readlines())
        lines.no_fnmatch_line("*run_helper1()*")


def test_traceback_style_default(testdir):
    testdir.makepyfile(
        """
        from pytest_check import check

        def run_helper2():
            with check("first fail"): assert 1 == 0
            with check("second fail"): assert 1 > 2
            with check("third fail"): assert 1 < 5 < 4

        def run_helper1():
            run_helper2()

        def test_failures():
            run_helper1()
    """
    )

    result = testdir.runpytest("--junitxml=output.xml")
    result.assert_outcomes(failed=1, passed=0)
    with open("output.xml") as f:
        lines = LineMatcher(f.readlines())
        lines.fnmatch_lines("*run_helper1()*")
