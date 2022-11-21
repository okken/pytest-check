import functools
import pytest
from .check_log import log_failure

__all__ = [
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
    "check_func",
]


_stop_on_fail = False


def set_stop_on_fail(stop_on_fail):
    global _stop_on_fail
    _stop_on_fail = stop_on_fail


def check_func(func):
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        __tracebackhide__ = True
        try:
            func(*args, **kwds)
            return True
        except AssertionError as e:
            if _stop_on_fail:
                raise e
            log_failure(e)
            return False

    return wrapper


@check_func
def equal(a, b, msg=""):
    assert a == b, msg


@check_func
def not_equal(a, b, msg=""):
    assert a != b, msg


@check_func
def is_(a, b, msg=""):
    assert a is b, msg


@check_func
def is_not(a, b, msg=""):
    assert a is not b, msg


@check_func
def is_true(x, msg=""):
    assert bool(x), msg


@check_func
def is_false(x, msg=""):
    assert not bool(x), msg


@check_func
def is_none(x, msg=""):
    assert x is None, msg


@check_func
def is_not_none(x, msg=""):
    assert x is not None, msg


@check_func
def is_in(a, b, msg=""):
    assert a in b, msg


@check_func
def is_not_in(a, b, msg=""):
    assert a not in b, msg


@check_func
def is_instance(a, b, msg=""):
    assert isinstance(a, b), msg


@check_func
def is_not_instance(a, b, msg=""):
    assert not isinstance(a, b), msg


@check_func
def almost_equal(a, b, rel=None, abs=None, msg=""):
    """
    for rel and abs tolerance, see:
    See https://docs.pytest.org/en/latest/builtin.html#pytest.approx
    """
    assert a == pytest.approx(b, rel, abs), msg


@check_func
def not_almost_equal(a, b, rel=None, abs=None, msg=""):
    """
    for rel and abs tolerance, see:
    See https://docs.pytest.org/en/latest/builtin.html#pytest.approx
    """
    assert a != pytest.approx(b, rel, abs), msg


@check_func
def greater(a, b, msg=""):
    assert a > b, msg


@check_func
def greater_equal(a, b, msg=""):
    assert a >= b, msg


@check_func
def less(a, b, msg=""):
    assert a < b, msg


@check_func
def less_equal(a, b, msg=""):
    assert a <= b, msg
