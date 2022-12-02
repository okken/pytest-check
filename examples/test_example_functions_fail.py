"""
Failing versions of all of the check helper functions.
"""
from pytest_check import check


def test_equal():
    check.equal(1, 2)


def test_not_equal():
    check.not_equal(1, 1)


def test_is():
    x = ["foo"]
    y = ["foo"]
    check.is_(x, y)


def test_is_not():
    x = ["foo"]
    y = x
    check.is_not(x, y)


def test_is_true():
    check.is_true(False)


def test_is_false():
    check.is_false(True)


def test_is_none():
    a = 1
    check.is_none(a)


def test_is_not_none():
    a = None
    check.is_not_none(a)


def test_is_in():
    check.is_in(4, [1, 2, 3])


def test_is_not_in():
    check.is_not_in(2, [1, 2, 3])


def test_is_instance():
    check.is_instance(1, str)


def test_is_not_instance():
    check.is_not_instance(1, int)


def test_almost_equal():
    check.almost_equal(1, 2)
    check.almost_equal(1, 2.1, abs=0.1)
    check.almost_equal(1, 3, rel=1)


def test_not_almost_equal():
    check.not_almost_equal(1, 1)
    check.not_almost_equal(1, 1.1, abs=0.1)
    check.not_almost_equal(1, 2, rel=1)


def test_greater():
    check.greater(1, 2)
    check.greater(1, 1)


def test_greater_equal():
    check.greater_equal(1, 2)


def test_less():
    check.less(2, 1)
    check.less(1, 1)


def test_less_equal():
    check.less_equal(2, 1)


def test_between():
    check.between(0, 0, 20)


def test_between_ge():
    check.between(20, 0, 20, ge=True)


def test_between_le():
    check.between(0, 0, 20, le=True)


def test_between_ge_le():
    check.between(21, 0, 20, ge=True, le=True)
