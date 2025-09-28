import pytest

from pytest_check import check


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
    result.assert_outcomes(passed=2, failed=2)
    result.stdout.fnmatch_lines(["* 2 failed, 2 passed *"])


@pytest.mark.xfail(raises=ZeroDivisionError)
def test_xfail_raises_should_fail():
    assert 1 == 2


@pytest.mark.xfail(raises=ZeroDivisionError)
def test_xfail_raises_should_fail_check():
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=ValueError)
@pytest.mark.xfail(raises=ZeroDivisionError)
def test_xfail_raises_check_multiple_unmatched_marks():
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=AssertionError)
@pytest.mark.xfail(raises=ZeroDivisionError)
def test_xfail_raises_check_multiple_marks():
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=ZeroDivisionError)
@pytest.mark.xfail(raises=AssertionError)
def test_xfail_raises_check_multiple_marks_reverse_order():
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=(ZeroDivisionError, AssertionError))
def test_xfail_raises_should_fail_check_tuple():
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=(ZeroDivisionError,))
def test_xfail_raises_should_fail_check_tuple_single_value():
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=(AssertionError,))
def test_xfail_raises_check_tuple_single_value():
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=AssertionError)
def test_xfail_raises_ok():
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=AssertionError)
def test_xfail_raises_ok_check():
    with check:
        assert 1 == 2
