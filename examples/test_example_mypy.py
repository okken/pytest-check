"""
Used by mypy to make sure that the type annotations are correct.

Normally you would import the check functions like this:
    from pytest_check import check

We're testing that an old form of import also works:
    import pytest_check as check

However, please be aware that this method of importing is deprecated and
support may be removed in future versions.

The original content of this file is from test_example_functions_pass.py.
But I've also added more tests to check for anything I want to get
tested with `mypy --strict`.
"""

import math
import importlib
from typing import Any
import pytest
import pytest_check as check

try:
    np: Any = importlib.import_module("numpy")
except ModuleNotFoundError:
    np = None


def test_equal() -> None:
    check.equal(1, 1)


def test_not_equal() -> None:
    check.not_equal(1, 2)


def test_is() -> None:
    x = ["foo"]
    y = x
    check.is_(x, y)


def test_is_nan() -> None:
    check.is_nan(math.nan)


def test_is_not_nan() -> None:
    check.is_not_nan(0)


def test_is_not() -> None:
    x = ["foo"]
    y = ["foo"]
    check.is_not(x, y)


def test_is_true() -> None:
    check.is_true(True)


def test_is_false() -> None:
    check.is_false(False)


def test_is_none() -> None:
    a = None
    check.is_none(a)


def test_is_not_none() -> None:
    a = 1
    check.is_not_none(a)


def test_is_in() -> None:
    check.is_in(2, [1, 2, 3])


def test_is_not_in() -> None:
    check.is_not_in(4, [1, 2, 3])


def test_is_instance() -> None:
    check.is_instance(1, int)


def test_is_not_instance() -> None:
    check.is_not_instance(1, str)


def test_almost_equal() -> None:
    check.almost_equal(1, 1)
    check.almost_equal(1, 1.1, abs=0.2)
    check.almost_equal(2, 1, rel=1)


def test_not_almost_equal() -> None:
    check.not_almost_equal(1, 2)
    check.not_almost_equal(1, 2.1, abs=0.1)
    check.not_almost_equal(3, 1, rel=1)


def test_greater() -> None:
    check.greater(2, 1)


def test_greater_equal() -> None:
    check.greater_equal(2, 1)
    check.greater_equal(1, 1)


def test_int_float() -> None:
    check.greater(2, 1.9)
    check.greater_equal(2, 1.9)
    check.less(1.9, 2)
    check.less_equal(1.9, 2)
    check.between(10, 4.5, 20)


def test_less() -> None:
    check.less(1, 2)


def test_less_equal() -> None:
    check.less_equal(1, 2)
    check.less_equal(1, 1)


def test_between() -> None:
    check.between(10, 0, 20)


def test_between_ge() -> None:
    check.between(10, 0, 20, ge=True)
    check.between(0, 0, 20, ge=True)


def test_between_le() -> None:
    check.between(10, 0, 20, le=True)
    check.between(20, 0, 20, le=True)


def test_between_ge_le() -> None:
    check.between(0, 0, 20, ge=True, le=True)
    check.between(10, 0, 20, ge=True, le=True)
    check.between(20, 0, 20, ge=True, le=True)


def test_between_equal() -> None:
    check.between_equal(0, 0, 20)
    check.between_equal(10, 0, 20)
    check.between_equal(20, 0, 20)


@pytest.mark.skipif(np is None, reason="numpy is not installed")
def test_greater_equal_max_int() -> None:
    if np is not None:
        check.greater_equal(np.iinfo(np.int32).max, 0)


@pytest.mark.skipif(np is None, reason="numpy is not installed")
def test_greater_equal_max_float() -> None:
    if np is not None:
        check.greater_equal(np.finfo(np.float32).max, 0)


@pytest.mark.skipif(np is None, reason="numpy is not installed")
def test_greater_max_int() -> None:
    if np is not None:
        check.greater(np.iinfo(np.int32).max, 0)


@pytest.mark.skipif(np is None, reason="numpy is not installed")
def test_less_min_float() -> None:
    if np is not None:
        check.less(np.finfo(np.float32).min, 0)


@pytest.mark.skipif(np is None, reason="numpy is not installed")
def test_less_equal_max_float() -> None:
    if np is not None:
        max_f32 = np.finfo(np.float32).max
        check.less_equal(max_f32, max_f32)
