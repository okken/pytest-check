
import pytest

# flake8: noqa


@pytest.fixture()
def example(testdir):
    testdir.makepyfile(
        """
        from pytest_check import check

        def test_func():
            helper1()


        def helper1():
            helper2()

        def helper2():
            with check("first"): assert 1 == 0
            with check("second"): assert 1 > 2
        """
    )


def test_sequence_with_helper_funcs(testdir, example):
    """
    Should show a sequence of calls 
    """
    result = testdir.runpytest()
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: first",
            "*in test_func() -> helper1()",
            "*in helper1() -> helper2()",
            '*in helper2() -> with check("first"): assert 1 == 0',
            "*FAILURE: second",
            "*in test_func() -> helper1()",
            "*in helper1() -> helper2()",
            '*in helper2() -> with check("second"): assert 1 > 2',
            "*Failed Checks: 2*",
        ]
    )
