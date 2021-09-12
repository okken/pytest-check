import pytest

# flake8: noqa


@pytest.fixture()
def example(testdir):
    testdir.makepyfile(
        """
        from pytest_check import check

        def test_a():
          with check:
            assert False, "one"
          with check:
            assert False, "two"
          with check:
            assert False, "three"

        def test_b():
            pass
        """
    )


def test_check_maxfail_1(testdir, example):
    """
    Should stop after first failed check
    """
    result = testdir.runpytest("--maxfail=1")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(["*AssertionError: one*"])


def test_check_maxfail_2(testdir, example):
    """
    Should not stop on checks.
    """
    result = testdir.runpytest("--maxfail=2")
    result.assert_outcomes(failed=1, passed=1)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: one",
            "*FAILURE: two",
            "*FAILURE: three",
            "*Failed Checks: 3*",
        ]
    )
