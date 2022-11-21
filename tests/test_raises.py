import pytest

from pytest_check import raises


class BaseTestException(Exception):
    pass


class _TestException(BaseTestException):
    pass


class AnotherTestException(BaseTestException):
    pass


BASE_IMPORTS_AND_EXCEPTIONS = """
from pytest_check import raises

class BaseTestException(Exception):
    pass


class _TestException(BaseTestException):
    pass


class AnotherTestException(BaseTestException):
    pass
"""


def test_raises():
    with raises(_TestException):
        raise _TestException


def test_raises_with_assertion_error():
    with raises(AssertionError):
        assert 0


def test_raises_with_multiple_errors(testdir):
    with raises((_TestException, AnotherTestException)):
        raise _TestException

    with raises((_TestException, AnotherTestException)):
        raise AnotherTestException

    testdir.makepyfile(
        BASE_IMPORTS_AND_EXCEPTIONS
        + """
def test_failures():
  with raises((_TestException, AnotherTestException)):
      raise AssertionError
"""
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.re_match_lines(
        [
            "FAILURE: ",
            # Python < 3.10 reports error at `raise` but 3.10 reports at `with`
            r".*raise AssertionError.*"
            r"|.*with raises\(\(_TestException, AnotherTestException\)\):.*",
        ],
        consecutive=True,
    )


def test_raises_with_parents_and_children(testdir):
    with raises(BaseTestException):
        raise _TestException

    with raises((BaseTestException, _TestException)):
        raise BaseTestException

    with raises((BaseTestException, _TestException)):
        raise _TestException

    # Children shouldn't catch their parents, only vice versa.
    testdir.makepyfile(
        BASE_IMPORTS_AND_EXCEPTIONS
        + """
def test_failures():
    with raises((_TestException, AnotherTestException)):
        raise BaseTestException
"""
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.re_match_lines(
        [
            "FAILURE: ",
            # Python < 3.10 reports error at `raise` but 3.10 reports at `with`
            r".*raise BaseTestException.*"
            r"|.*with raises\(\(_TestException, AnotherTestException\)\):.*",
        ],
        consecutive=True,
    )


@pytest.mark.parametrize(
    "run_flags,match_lines",
    [
        ("--exitfirst", ["test_raises_stop_on_fail.py:19: ValueError"]),
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
        BASE_IMPORTS_AND_EXCEPTIONS
        + """
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


def test_can_mix_assertions_and_checks(pytester):
    """
    You can mix checks and asserts, but a failing assert stops test execution.
    """
    pytester.copy_example("examples/test_example_mix_checks_and_assertions.py")
    result = pytester.runpytest()
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE:*",
            "*Failed Checks: 1*",
            "*assert 1 == 2*",
        ]
    )


def test_msg_kwarg_with_raises_context_manager(testdir):
    testdir.makepyfile(
        """
        from pytest_check import raises

        def raise_valueerror():
            raise ValueError

        def test():
            with raises(AssertionError, msg="hello, world!"):
                raise_valueerror()
    """
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["FAILURE: hello, world!"])


def test_raises_function(testdir):
    def raise_error():
        raise _TestException

    # Single exception
    raises(_TestException, raise_error)

    # Multiple exceptions
    raises((_TestException, AnotherTestException), raise_error)

    def assert_foo_equals_bar(foo, bar=None):
        assert foo == bar

    # Test args and kwargs are passed to callable
    raises(AssertionError, assert_foo_equals_bar, 1, bar=2)

    # Kwarg `msg` is special and can be found in failure output.
    testdir.makepyfile(
        """
        from pytest_check import raises

        def raise_valueerror():
            raise ValueError

        def test():
            raises(AssertionError, raise_valueerror, msg="hello, world!")
    """
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["FAILURE: hello, world!"])
