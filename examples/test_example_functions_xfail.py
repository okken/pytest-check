"""
Failing versions of all of the check helper functions, each marked with xfail.
"""

from pytest_check import check
import math


def test_equal():
    check.equal(1, 2, xfail="xfail-equal")


def test_not_equal():
    check.not_equal(1, 1, xfail="xfail-not_equal")


def test_is():
    x = ["foo"]
    y = ["foo"]
    check.is_(x, y, xfail="xfail-is")


def test_is_not():
    x = ["foo"]
    y = x
    check.is_not(x, y, xfail="xfail-is_not")


def test_is_nan():
    check.is_nan(42, xfail="xfail-is_nan")


def test_is_not_nan():
    check.is_not_nan(math.nan, xfail="xfail-is_not_nan")


def test_is_true():
    check.is_true(False, xfail="xfail-is_true")


def test_is_false():
    check.is_false(True, xfail="xfail-is_false")


def test_is_none():
    a = 1
    check.is_none(a, xfail="xfail-is_none")


def test_is_not_none():
    a = None
    check.is_not_none(a, xfail="xfail-is_not_none")


def test_is_in():
    check.is_in(4, [1, 2, 3], xfail="xfail-is_in")


def test_is_not_in():
    check.is_not_in(2, [1, 2, 3], xfail="xfail-is_not_in")


def test_is_instance():
    check.is_instance(1, str, xfail="xfail-is_instance")


def test_is_not_instance():
    check.is_not_instance(1, int, xfail="xfail-is_not_instance")


def test_almost_equal():
    check.almost_equal(1, 2, xfail="xfail-almost_equal-1")
    check.almost_equal(1, 2.1, abs=0.1, xfail="xfail-almost_equal-2")
    check.almost_equal(1, 3, rel=1, xfail="xfail-almost_equal-3")


def test_not_almost_equal():
    check.not_almost_equal(1, 1, xfail="xfail-not_almost_equal-1")
    check.not_almost_equal(1, 1.1, abs=0.1, xfail="xfail-not_almost_equal-2")
    check.not_almost_equal(1, 2, rel=1, xfail="xfail-not_almost_equal-3")


def test_greater():
    check.greater(1, 2, xfail="xfail-greater-1")
    check.greater(1, 1, xfail="xfail-greater-2")


def test_greater_equal():
    check.greater_equal(1, 2, xfail="xfail-greater_equal")


def test_less():
    check.less(2, 1, xfail="xfail-less-1")
    check.less(1, 1, xfail="xfail-less-2")


def test_less_equal():
    check.less_equal(2, 1, xfail="xfail-less_equal")


def test_between():
    check.between(0, 0, 20, xfail="xfail-between")


def test_between_ge():
    check.between(20, 0, 20, ge=True, xfail="xfail-between-ge")


def test_between_le():
    check.between(0, 0, 20, le=True, xfail="xfail-between-le")


def test_between_ge_le():
    check.between(21, 0, 20, ge=True, le=True, xfail="xfail-between-ge-le")


def test_between_equal():
    check.between_equal(21, 0, 20, xfail="xfail-between_equal")
