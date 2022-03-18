import functools
import inspect
import os
import pytest

__all__ = [
    "check",
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
    "raises",
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

    msg = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        __tracebackhide__ = True
        if exc_type is not None and issubclass(exc_type, AssertionError):
            if _stop_on_fail:
                self.msg = None
                return
            else:
                if self.msg is not None:
                    log_failure(self.msg)
                else:
                    log_failure(exc_val)
                self.msg = None
                return True
        self.msg = None

    def __call__(self, msg=None):
        self.msg = msg
        return self


check = CheckContextManager()


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


def raises(expected_exception, *args, **kwargs):
    """
    Check that a given callable or context raises an error of a given type.

    Can be used as either a context manager:

    >>> with raises(AssertionError):
    >>>     raise AssertionError

    or as a function:

    >>> def raises_assert():
    >>>     raise AssertionError
    >>> raises(AssertionError, raises_assert)

    `expected_exception` follows the same format rules as the second argument
    to `issubclass`, so multiple possible exception types can be used.

    When args[0] is callable, the remainder of args and all of kwargs except
    for any called `msg` are passed to args[0] as arguments.

    Note that because `raises` is implemented using a context manager, the
    usual control flow warnings apply: within the context, execution stops on
    the first error encountered *and does not resume after this error has been
    logged*.  Therefore, the line you expect to raise an error must be the last
    line of the context: any subsequent lines won't be executed.  Pull such
    lines out of the context if they don't raise errors, or use more calls to
    `raises` if they do.

    This function is modeled loosely after Pytest's own `raises`, except for
    the latter's `match`-ing logic.  We should strive to keep the call
    signature of this `raises` as close as possible to the other `raises`.
    """
    __tracebackhide__ = True

    if isinstance(expected_exception, type):
        excepted_exceptions = (expected_exception,)
    else:
        excepted_exceptions = expected_exception

    assert all(
        isinstance(exc, type) or issubclass(exc, BaseException)
        for exc in excepted_exceptions
    )

    msg = kwargs.pop("msg", None)
    if not args:
        assert not kwargs, (
            f"Unexpected kwargs for pytest_check.raises: {kwargs}"
        )
        return CheckRaisesContext(expected_exception, msg=msg)
    else:
        func = args[0]
        assert callable(func)
        with CheckRaisesContext(expected_exception, msg=msg):
            func(*args[1:], **kwargs)


class CheckRaisesContext:
    """
    Helper context for `raises` that can be parameterized by error type.

    Note that CheckRaisesContext is instantiated whenever needed; it is not a
    global variable like `check`.  Therefore, we don't need to curate
    `self.msg` in `__exit__` for this class like we do with
    CheckContextManager.
    """

    def __init__(self, *expected_excs, msg=None):
        self.expected_excs = expected_excs
        self.msg = msg

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        __tracebackhide__ = True
        if exc_type is not None and issubclass(exc_type, self.expected_excs):
            # This is the case where an error has occured within the context
            # but it is the type we're expecting.  Therefore we return True
            # to silence this error and proceed with execution outside the
            # context.
            return True

        if not _stop_on_fail:
            # Returning something falsey here will cause the context
            # manager to *not* suppress an exception not in
            # `expected_excs`, thus allowing the higher-level Pytest
            # context to handle it like any other unhandle exception during
            # test execution, including display and tracebacks.  That is the
            # behavior we want when `_stop_on_fail` is True, so we let that
            # case fall through.  If *not* `_stop_on_fail`, then we want to
            # log the error as a failed check but then continue execution
            # without raising an error, hence `return True`.
            log_failure(self.msg if self.msg else exc_val)
            return True


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
        line = "{}:{} in {}() -> {}".format(file, line, func, context)
        pseudo_trace.append(line)
        level += 1
    pseudo_trace_str = "\n".join(reversed(pseudo_trace))
    entry = "FAILURE: {}\n{}".format(msg if msg else "", pseudo_trace_str)
    _failures.append(entry)
