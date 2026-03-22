from pytest_check import check
import pytest


# TODO: we may add xpass support in the future,
# but it may slow down the common case of xfail checks that pass, 
# so we want to consider carefully before adding it.

# Have a check function xfail
# Failures -> xfail result 
# Passes -> pass result (not xpass)
def test_should_xfail_func_xfail():
    "should xfail"
    check.equal(1, 2, xfail='func reason')

def test_should_pass_func_xfail():
    "should pass"
    check.equal(1, 1, xfail='func reason')


# marked as xfail + have check function xfail
# Failures -> xfail result 
# Passes -> xpass result (handled by mark, not check)

@pytest.mark.xfail(reason='xfail reason')
def test_should_xfail__mark_xfail_func_xfail():
    "should xfail"
    check.equal(1, 2, xfail='func reason')

@pytest.mark.xfail(reason='xfail reason')
def test_should_xpass__mark_xfail_func_xfail():
    "should xpass"
    check.equal(1, 1, xfail='func reason')

# have check function xfail + an assertion failure
# check function fails -> fail result (due to assertion failure)
# check function passes -> fail result (due to assertion failure)

def test_should_fail__xfail_pass_assert_fail():
    "should fail"
    check.equal(1, 1, xfail='func reason')
    assert 1 == 2, "assert reason"

def test_should_fail__xfail_fail_assert_fail():
    "should fail"
    check.equal(1, 2, xfail='func reason')
    assert 1 == 2, "assert reason"
