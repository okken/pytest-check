from __future__ import annotations
from typing import Iterable, Any

from .check_log import log_failure

_stop_on_fail = False


# TODO: Returning Any isn't ideal, but returning CheckRaisesContext | None
#  would require callers to type ignore or declare the type when using `with`.
#  Or, it could always return CheckRaisesContext, just an empty one after
#  calling the passed function.
def raises(
    expected_exception: type | Iterable[type], *args: Any, **kwargs: object
) -> Any:
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
        expected_exceptions: Iterable[type] = (expected_exception,)
    else:
        expected_exceptions = expected_exception

    assert all(
        isinstance(exc, type) or issubclass(exc, BaseException)
        for exc in expected_exceptions
    )

    msg = kwargs.pop("msg", None)
    if not args:
        assert not kwargs, f"Unexpected kwargs for pytest_check.raises: {kwargs}"
        return CheckRaisesContext(*expected_exceptions, msg=msg)
    else:
        func = args[0]
        assert callable(func)
        with CheckRaisesContext(*expected_exceptions, msg=msg):
            func(*args[1:], **kwargs)


class CheckRaisesContext:
    """
    Helper context for `raises` that can be parameterized by error type.

    Note that CheckRaisesContext is instantiated whenever needed; it is not a
    global variable like `check`.  Therefore, we don't need to curate
    `self.msg` in `__exit__` for this class like we do with
    CheckContextManager.
    """

    def __init__(self, *expected_excs: type, msg: object = None) -> None:
        self.expected_excs = expected_excs
        self.msg = msg
        self.value: object | None = None

    def __enter__(self) -> "CheckRaisesContext":
        return self

    def __exit__(self, exc_type: type, exc_val: object, exc_tb: object) -> bool:
        __tracebackhide__ = True

        self.value = exc_val
        if exc_type is not None and issubclass(exc_type, self.expected_excs):
            # This is the case where an error has occured within the context,
            # but it is the type we're expecting.  Therefore, we return True
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

        # Stop on fail, so return False
        return False
