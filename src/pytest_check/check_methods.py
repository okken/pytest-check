import functools
import inspect
import os
import pytest


__all__ = [
    "check",
    "equal",
    "not_equal",
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
    "check_func"
]


_stop_on_fail = False
_failures = []


def clear_failures():
    global _failures
    _failures = []


def get_failures():
    return _failures


def set_stop_on_fail(stop_on_fail):
    global _stop_on_fail
    _stop_on_fail = stop_on_fail


class CheckContextManager(object):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        __tracebackhide__ = True
        if exc_type is not None and issubclass(exc_type, AssertionError):
            if _stop_on_fail:
                return
            else:
                log_failure(exc_val)
                return True


check = CheckContextManager()


def check_func(func):
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        __tracebackhide__ = True
        try:
            func(*args, **kwds)
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


def get_full_context(level):
    (_, filename, line, funcname, contextlist) = inspect.stack()[level][0:5]
    filename = os.path.relpath(filename)
    context = contextlist[0].strip()
    return (filename, line, funcname, context)


def log_failure(msg):
    __tracebackhide__ = True
    level = 3
    pseudo_trace = []
    func = ""
    while "test_" not in func:
        (file, line, func, context) = get_full_context(level)
        if "site-packages" in file:
            break
        line = "  {}, line {}, in {}() -> {}".format(file, line, func, context)
        pseudo_trace.append(line)
        level += 1
    pseudo_trace_str = "\n".join(reversed(pseudo_trace))
    entry = "FAILURE: {}\n{}".format(msg if msg else "", pseudo_trace_str)
    _failures.append(entry)
