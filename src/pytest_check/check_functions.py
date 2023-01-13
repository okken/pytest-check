import functools

import pytest

from .check_log import log_failure

__all__ = [
    "assert_equal",
    "equal",
    "not_equal",
    "is_",
    "is_not",
    "is_true",
    "is_false",
    "is_none",
    "is_not_none",
    "is_in",
    "is_not_in",
    "is_instance",
    "is_not_instance",
    "almost_equal",
    "not_almost_equal",
    "greater",
    "greater_equal",
    "less",
    "less_equal",
    "between",
    "check_func",
]


def check_func(func):
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        __tracebackhide__ = True
        try:
            func(*args, **kwds)
            return True
        except AssertionError as e:
            log_failure(e)
            return False

    return wrapper


def assert_equal(a, b, msg=""):  # pragma: no cover
    assert a == b, msg


def equal(a, b, msg=""):
    __tracebackhide__ = True
    if a == b:
        return True
    else:
        log_failure(f"check {a} == {b}", msg)
        return False


def not_equal(a, b, msg=""):
    __tracebackhide__ = True
    if a != b:
        return True
    else:
        log_failure(f"check {a} != {b}", msg)
        return False


def is_(a, b, msg=""):
    __tracebackhide__ = True
    if a is b:
        return True
    else:
        log_failure(f"check {a} is {b}", msg)
        return False


def is_not(a, b, msg=""):
    __tracebackhide__ = True
    if a is not b:
        return True
    else:
        log_failure(f"check {a} is not {b}", msg)
        return False


def is_true(x, msg=""):
    __tracebackhide__ = True
    if bool(x):
        return True
    else:
        log_failure(f"check bool({x})", msg)
        return False


def is_false(x, msg=""):
    __tracebackhide__ = True
    if not bool(x):
        return True
    else:
        log_failure(f"check not bool({x})", msg)
        return False


def is_none(x, msg=""):
    __tracebackhide__ = True
    if x is None:
        return True
    else:
        log_failure(f"check {x} is None", msg)
        return False


def is_not_none(x, msg=""):
    __tracebackhide__ = True
    if x is not None:
        return True
    else:
        log_failure(f"check {x} is not None", msg)
        return False


def is_in(a, b, msg=""):
    __tracebackhide__ = True
    if a in b:
        return True
    else:
        log_failure(f"check {a} in {b}", msg)
        return False


def is_not_in(a, b, msg=""):
    __tracebackhide__ = True
    if a not in b:
        return True
    else:
        log_failure(f"check {a} not in {b}", msg)
        return False


def is_instance(a, b, msg=""):
    __tracebackhide__ = True
    if isinstance(a, b):
        return True
    else:
        log_failure(f"check isinstance({a}, {b})", msg)
        return False


def is_not_instance(a, b, msg=""):
    __tracebackhide__ = True
    if not isinstance(a, b):
        return True
    else:
        log_failure(f"check not isinstance({a}, {b})", msg)
        return False


def almost_equal(a, b, rel=None, abs=None, msg=""):
    """
    For rel and abs tolerance, see:
    See https://docs.pytest.org/en/latest/builtin.html#pytest.approx
    """
    __tracebackhide__ = True
    if a == pytest.approx(b, rel, abs):
        return True
    else:
        log_failure(f"check {a} == pytest.approx({b}, rel={rel}, abs={abs})", msg)
        return False


def not_almost_equal(a, b, rel=None, abs=None, msg=""):
    """
    For rel and abs tolerance, see:
    See https://docs.pytest.org/en/latest/builtin.html#pytest.approx
    """
    __tracebackhide__ = True
    if a != pytest.approx(b, rel, abs):
        return True
    else:
        log_failure(f"check {a} != pytest.approx({b}, rel={rel}, abs={abs})", msg)
        return False


def greater(a, b, msg=""):
    __tracebackhide__ = True
    if a > b:
        return True
    else:
        log_failure(f"check {a} > {b}", msg)
        return False


def greater_equal(a, b, msg=""):
    __tracebackhide__ = True
    if a >= b:
        return True
    else:
        log_failure(f"check {a} >= {b}", msg)
        return False


def less(a, b, msg=""):
    __tracebackhide__ = True
    if a < b:
        return True
    else:
        log_failure(f"check {a} < {b}", msg)
        return False


def less_equal(a, b, msg=""):
    __tracebackhide__ = True
    if a <= b:
        return True
    else:
        log_failure(f"check {a} <= {b}", msg)
        return False


def between(b, a, c, msg="", ge=False, le=False):
    __tracebackhide__ = True
    if ge and le:
        if a <= b <= c:
            return True
        else:
            log_failure(f"check {a} <= {b} <= {c}", msg)
            return False
    elif ge:
        if a <= b < c:
            return True
        else:
            log_failure(f"check {a} <= {b} < {c}", msg)
            return False
    elif le:
        if a < b <= c:
            return True
        else:
            log_failure(f"check {a} < {b} <= {c}", msg)
            return False
    else:
        if a < b < c:
            return True
        else:
            log_failure(f"check {a} < {b} < {c}", msg)
            return False
