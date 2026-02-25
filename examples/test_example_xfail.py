"""
Ensure that xfail, both strict and not strict,
behaves correctly for check passes/failures.
"""

import pytest

from pytest_check import check


@pytest.mark.xfail()
def test_xfail():
    "Should xfail"
    check.equal(1, 2)


@pytest.mark.xfail(strict=True)
def test_xfail_strict():
    "Should xfail"
    check.equal(1, 2)


@pytest.mark.xfail()
def test_xfail_pass():
    "Should xpass"
    check.equal(1, 1)


@pytest.mark.xfail(strict=True)
def test_xfail_pass_strict():
    "Should fail (xpass strict)"
    check.equal(1, 1)


@pytest.mark.xfail(raises=ZeroDivisionError)
def test_xfail_raises_should_fail_check():
    "Should fail"
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=ValueError)
@pytest.mark.xfail(raises=ZeroDivisionError)
def test_xfail_raises_check_multiple_unmatched_marks():
    "Should fail"
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=(ZeroDivisionError,))
def test_xfail_raises_should_fail_check_tuple_single_value():
    "Should fail"
    with check:
        assert 1 == 2


@pytest.mark.xfail()
def test_xfail_no_raises_with_check():
    "Should xfail"
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=AssertionError)
def test_xfail_raises_assertion_error_matches():
    "Should xfail"
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=(ValueError, AssertionError))
def test_xfail_raises_tuple_matches():
    "Should xfail"
    with check:
        assert 1 == 2


@pytest.mark.xfail(raises=AssertionError)
@pytest.mark.xfail(raises=ZeroDivisionError)
def test_xfail_raises_multiple_marks_one_matches():
    "Should xfail"
    with check:
        assert 1 == 2
