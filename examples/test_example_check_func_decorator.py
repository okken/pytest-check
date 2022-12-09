"""
Make sure the @check.check_func decorator works.
"""

from pytest_check import check


@check.check_func
def is_five(a):
    assert a == 5


def test_pass():
    is_five(5)


def test_pass_return_val_of_check_helper():
    assert is_five(5) is True


@check.check_func
def is_four(a):
    assert a == 4


def test_all_four():
    is_four(1)
    is_four(2)
    should_be_False = is_four(3)
    should_be_True = is_four(4)
    print(f"should_be_True={should_be_True}")
    print(f"should_be_False={should_be_False}")
