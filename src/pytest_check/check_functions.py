from __future__ import annotations
import functools
import sys
from typing import (
    Any,
    Callable,
    Container,
    Protocol,
    SupportsFloat,
    SupportsIndex,
    TypeVar,
    Union,
    overload,
)

if sys.version_info < (3, 10):  # pragma: no cover
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

import pytest
import math
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
    "is_nan",
    "is_not_nan",
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
    "between_equal",
    "check_func",
    "fail",
]


_P = ParamSpec("_P")
_T = TypeVar("_T")

_CmpT = TypeVar("_CmpT", contravariant=True)


class _ComparableGreaterThan(Protocol[_CmpT]):
    def __gt__(self, other: _CmpT, /) -> bool: ...  # pragma: no cover


class _ComparableGreaterThanOrEqual(Protocol[_CmpT]):
    def __ge__(self, other: _CmpT, /) -> bool: ...  # pragma: no cover


class _ComparableLessThan(Protocol[_CmpT]):
    def __lt__(self, other: _CmpT, /) -> bool: ...  # pragma: no cover


class _ComparableLessThanOrEqual(Protocol[_CmpT]):
    def __le__(self, other: _CmpT, /) -> bool: ...  # pragma: no cover


def check_func(func: Callable[_P, _T]) -> Callable[_P, bool]:
    @functools.wraps(func)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> bool:
        __tracebackhide__ = True
        try:
            func(*args, **kwargs)
            return True
        except AssertionError as e:
            log_failure(e)
            return False

    return wrapper


def assert_equal(a: object, b: object, msg: str = "") -> None:  # pragma: no cover
    assert a == b, msg


def equal(a: object, b: object, msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if a == b:
        return True
    else:
        log_failure(f"check {a} == {b}", msg, xfail=xfail)
        return False


def not_equal(a: object, b: object, msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if a != b:
        return True
    else:
        log_failure(f"check {a} != {b}", msg, xfail=xfail)
        return False


def is_(a: object, b: object, msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if a is b:
        return True
    else:
        log_failure(f"check {a} is {b}", msg, xfail=xfail)
        return False


def is_not(a: object, b: object, msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if a is not b:
        return True
    else:
        log_failure(f"check {a} is not {b}", msg, xfail=xfail)
        return False


def is_true(x: object, msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if bool(x):
        return True
    else:
        log_failure(f"check bool({x})", msg, xfail=xfail)
        return False


def is_false(x: object, msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if not bool(x):
        return True
    else:
        log_failure(f"check not bool({x})", msg, xfail=xfail)
        return False


def is_none(x: object, msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if x is None:
        return True
    else:
        log_failure(f"check {x} is None", msg, xfail=xfail)
        return False


def is_not_none(x: object, msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if x is not None:
        return True
    else:
        log_failure(f"check {x} is not None", msg, xfail=xfail)
        return False


def is_nan(
    a: SupportsFloat | SupportsIndex, msg: str = "", xfail: str | None = None
) -> bool:
    __tracebackhide__ = True
    if math.isnan(a):
        return True
    else:
        log_failure(f"check {a} is NaN", msg, xfail=xfail)
        return False


def is_not_nan(
    a: SupportsFloat | SupportsIndex, msg: str = "", xfail: str | None = None
) -> bool:
    __tracebackhide__ = True
    if not math.isnan(a):
        return True
    else:
        log_failure(f"check {a} is not NaN", msg, xfail=xfail)
        return False


def is_in(a: _T, b: Container[_T], msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if a in b:
        return True
    else:
        log_failure(f"check {a} in {b}", msg, xfail=xfail)
        return False


def is_not_in(a: _T, b: Container[_T], msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if a not in b:
        return True
    else:
        log_failure(f"check {a} not in {b}", msg, xfail=xfail)
        return False


_TypeTuple = Union[type, tuple["_TypeTuple", ...]]


def is_instance(
    a: object, b: _TypeTuple, msg: str = "", xfail: str | None = None
) -> bool:
    __tracebackhide__ = True
    if isinstance(a, b):
        return True
    else:
        log_failure(f"check isinstance({a}, {b})", msg, xfail=xfail)
        return False


def is_not_instance(
    a: object, b: _TypeTuple, msg: str = "", xfail: str | None = None
) -> bool:
    __tracebackhide__ = True
    if not isinstance(a, b):
        return True
    else:
        log_failure(f"check not isinstance({a}, {b})", msg, xfail=xfail)
        return False


def almost_equal(
    a: object,
    b: object,
    rel: Any = None,
    abs: Any = None,
    msg: str = "",
    xfail: str | None = None,
) -> bool:
    """
    For rel and abs tolerance, see:
    See https://docs.pytest.org/en/latest/builtin.html#pytest.approx
    """
    __tracebackhide__ = True
    if a == pytest.approx(b, rel, abs):
        return True
    else:
        log_failure(
            f"check {a} == pytest.approx({b}, rel={rel}, abs={abs})", msg, xfail=xfail
        )
        return False


def not_almost_equal(
    a: object,
    b: object,
    rel: Any = None,
    abs: Any = None,
    msg: str = "",
    xfail: str | None = None,
) -> bool:
    """
    For rel and abs tolerance, see:
    See https://docs.pytest.org/en/latest/builtin.html#pytest.approx
    """
    __tracebackhide__ = True
    if a != pytest.approx(b, rel, abs):
        return True
    else:
        log_failure(
            f"check {a} != pytest.approx({b}, rel={rel}, abs={abs})", msg, xfail=xfail
        )
        return False


@overload
def greater(a: float, b: float, msg: str = "", xfail: str | None = None) -> bool: ...


@overload
def greater(
    a: SupportsFloat | SupportsIndex,
    b: SupportsFloat | SupportsIndex,
    msg: str = "",
    xfail: str | None = None,
) -> bool: ...


@overload
def greater(
    a: _ComparableGreaterThan[_CmpT], b: _CmpT, msg: str = "", xfail: str | None = None
) -> bool: ...


def greater(a: Any, b: Any, msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if a is None or b is None:
        log_failure(f"check {a} > {b}: None cannot be compared", msg, xfail=xfail)
        return False
    elif a > b:
        return True
    else:
        log_failure(f"check {a} > {b}", msg, xfail=xfail)
        return False


@overload
def greater_equal(
    a: float, b: float, msg: str = "", xfail: str | None = None
) -> bool: ...


@overload
def greater_equal(
    a: SupportsFloat | SupportsIndex,
    b: SupportsFloat | SupportsIndex,
    msg: str = "",
    xfail: str | None = None,
) -> bool: ...


@overload
def greater_equal(
    a: _ComparableGreaterThanOrEqual[_CmpT],
    b: _CmpT,
    msg: str = "",
    xfail: str | None = None,
) -> bool: ...


def greater_equal(a: Any, b: Any, msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if a is None or b is None:
        log_failure(f"check {a} >= {b}: None cannot be compared", msg, xfail=xfail)
        return False
    elif a >= b:
        return True
    else:
        log_failure(f"check {a} >= {b}", msg, xfail=xfail)
        return False


@overload
def less(a: float, b: float, msg: str = "", xfail: str | None = None) -> bool: ...


@overload
def less(
    a: SupportsFloat | SupportsIndex,
    b: SupportsFloat | SupportsIndex,
    msg: str = "",
    xfail: str | None = None,
) -> bool: ...


@overload
def less(
    a: _ComparableLessThan[_CmpT], b: _CmpT, msg: str = "", xfail: str | None = None
) -> bool: ...


def less(a: Any, b: Any, msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if a is None or b is None:
        log_failure(f"check {a} < {b}: None cannot be compared", msg, xfail=xfail)
        return False
    elif a < b:
        return True
    else:
        log_failure(f"check {a} < {b}", msg, xfail=xfail)
        return False


@overload
def less_equal(a: float, b: float, msg: str = "", xfail: str | None = None) -> bool: ...


@overload
def less_equal(
    a: SupportsFloat | SupportsIndex,
    b: SupportsFloat | SupportsIndex,
    msg: str = "",
    xfail: str | None = None,
) -> bool: ...


@overload
def less_equal(
    a: _ComparableLessThanOrEqual[_CmpT],
    b: _CmpT,
    msg: str = "",
    xfail: str | None = None,
) -> bool: ...


def less_equal(a: Any, b: Any, msg: str = "", xfail: str | None = None) -> bool:
    __tracebackhide__ = True
    if a is None or b is None:
        log_failure(f"check {a} <= {b}: None cannot be compared", msg, xfail=xfail)
        return False
    elif a <= b:
        return True
    else:
        log_failure(f"check {a} <= {b}", msg, xfail=xfail)
        return False


@overload
def between(
    b: float,
    a: float,
    c: float,
    msg: str = "",
    ge: bool = False,
    le: bool = False,
    xfail: str | None = None,
) -> bool: ...


@overload
def between(
    b: SupportsFloat | SupportsIndex,
    a: SupportsFloat | SupportsIndex,
    c: SupportsFloat | SupportsIndex,
    msg: str = "",
    ge: bool = False,
    le: bool = False,
    xfail: str | None = None,
) -> bool: ...


@overload
def between(
    b: _ComparableLessThanOrEqual[_CmpT],
    a: _CmpT,
    c: _CmpT,
    msg: str = "",
    ge: bool = False,
    le: bool = False,
    xfail: str | None = None,
) -> bool: ...


def between(
    b: Any,
    a: Any,
    c: Any,
    msg: str = "",
    ge: bool = False,
    le: bool = False,
    xfail: str | None = None,
) -> bool:
    __tracebackhide__ = True
    if a is None or b is None or c is None:
        log_failure(
            f"check {a} <= {b} <= {c}: None cannot be compared", msg, xfail=xfail
        )
        return False
    elif ge and le:
        if a <= b <= c:
            return True
        else:
            log_failure(f"check {a} <= {b} <= {c}", msg, xfail=xfail)
            return False
    elif ge:
        if a <= b < c:
            return True
        else:
            log_failure(f"check {a} <= {b} < {c}", msg, xfail=xfail)
            return False
    elif le:
        if a < b <= c:
            return True
        else:
            log_failure(f"check {a} < {b} <= {c}", msg, xfail=xfail)
            return False
    else:
        if a < b < c:
            return True
        else:
            log_failure(f"check {a} < {b} < {c}", msg, xfail=xfail)
            return False


@overload
def between_equal(
    b: float, a: float, c: float, msg: str = "", xfail: str | None = None
) -> bool: ...


@overload
def between_equal(
    b: SupportsFloat | SupportsIndex,
    a: SupportsFloat | SupportsIndex,
    c: SupportsFloat | SupportsIndex,
    msg: str = "",
    xfail: str | None = None,
) -> bool: ...


@overload
def between_equal(
    b: _ComparableLessThanOrEqual[_CmpT],
    a: _CmpT,
    c: _CmpT,
    msg: str = "",
    xfail: str | None = None,
) -> bool: ...


def between_equal(
    b: Any,
    a: Any,
    c: Any,
    msg: str = "",
    xfail: str | None = None,
) -> bool:
    __tracebackhide__ = True
    return between(b, a, c, msg, ge=True, le=True, xfail=xfail)


def fail(msg: str, xfail: str | None = None) -> None:
    __tracebackhide__ = True
    log_failure(msg, xfail=xfail)
