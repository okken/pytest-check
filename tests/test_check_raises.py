import pytest

from pytest_check import raises


class BaseTestException(Exception):
    pass


class TestException(BaseTestException):
    __test__ = False


class AnotherTestException(BaseTestException):
    pass


def test_raises():
    with raises(TestException):
        raise TestException


def test_raises_with_assertion_error():
    with raises(AssertionError):
        assert 0


def test_raises_with_multiple_errors(testdir):
    with raises(TestException, AnotherTestException):
        raise TestException

    with raises(TestException, AnotherTestException):
        raise AnotherTestException

    testdir.makepyfile(
        """
        from pytest_check import raises

        class BaseTestException(Exception):
            pass


        class TestException(BaseTestException):
            __test__ = False


        class AnotherTestException(BaseTestException):
            pass

        def test_failures():
            with raises(TestException, AnotherTestException):
                raise AssertionError
    """
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        ["*FAILURE: ", "*raise AssertionError*"], consecutive=True,
    )


def test_raises_with_parents_and_children(testdir):
    with raises(BaseTestException):
        raise TestException

    with raises(BaseTestException, TestException):
        raise BaseTestException

    with raises(BaseTestException, TestException):
        raise TestException

    # Children shouldn't catch their parents, only vice versa.
    testdir.makepyfile(
        """
        from pytest_check import raises

        class BaseTestException(Exception):
            pass


        class TestException(BaseTestException):
            __test__ = False


        class AnotherTestException(BaseTestException):
            pass

        def test_failures():
            with raises(TestException, AnotherTestException):
                raise BaseTestException
    """
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        ["*FAILURE: ", "*raise BaseTestException*"], consecutive=True,
    )


@pytest.mark.parametrize(
    "run_flags,match_lines",
    [
        ("--exitfirst", ["test_raises_stop_on_fail.py:15: ValueError"]),
        ("", ["*Failed Checks: 2*"]),
    ],
)
def test_raises_stop_on_fail(run_flags, match_lines, testdir):
    """
    Test multiple failures with and without `--exitfirst`

    With `--exitfirst`, first error is the only one reported, and without,
    multiple errors are accumulated.
    """
    # test_failures below includes one passed check, two checked failures, and
    # a final passed check.  `--exitfirst` should result in only the first
    # error reported, and subsequent errors and successes are ignored.  Without
    # that flag, two failures should be counted and reported, and the last
    # success should be executed.
    testdir.makepyfile(
        """
        from pytest_check import raises

        class BaseTestException(Exception):
            pass


        class TestException(BaseTestException):
            __test__ = False

        def test_failures():
            with raises(BaseTestException):
                raise BaseTestException

            with raises(BaseTestException):
                raise ValueError

            with raises(BaseTestException):
                raise ValueError

            with raises(BaseTestException):
                raise BaseTestException
    """
    )

    result = testdir.runpytest(run_flags)
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(match_lines)


def test_can_mix_assertions_and_checks(testdir):
    """
    You can mix checks and asserts, but a failing assert stops test execution.
    """
    testdir.makepyfile(
        """
        import pytest_check as check

        from pytest_check import raises

        def test_failures():
            assert 0 == 0

            check.equal(1, 1)

            check.equal(0, 1)

            assert 1 == 2

            check.equal(2, 3)
    """
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=1)
    # Accumulated check fails are reported up to assert failure, but not after.
    result.stdout.fnmatch_lines(["*Failed Checks: 1*"])
    result.stdout.fnmatch_lines(
        ["*FAILURE: ", "assert 0 == 1"], consecutive=True,
    )

    # Regular assert errors are reported as usual.
    result.stdout.fnmatch_lines(["E * assert 1 == 2"])
