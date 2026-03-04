from __future__ import annotations

from typing import (
    Any,
    Callable,
    Protocol,
    SupportsFloat,
    SupportsIndex,
    TypeVar,
    overload,
)

from .context_manager import CheckContextManager as _BaseCheck
from .check_functions import (
    assert_equal,
    equal,
    not_equal,
    is_,
    is_not,
    is_true,
    is_false,
    is_none,
    is_not_none,
    is_nan,
    is_not_nan,
    is_in,
    is_not_in,
    is_instance,
    is_not_instance,
    almost_equal,
    not_almost_equal,
    greater,
    greater_equal,
    less,
    less_equal,
    between,
    between_equal,
    check_func,
    fail,
)
from .check_raises import raises
from .check_log import any_failures

_CmpT = TypeVar("_CmpT", contravariant=True)

class _ComparableGreaterThan(Protocol[_CmpT]):
    def __gt__(self, other: _CmpT, /) -> bool: ...

class _ComparableGreaterThanOrEqual(Protocol[_CmpT]):
    def __ge__(self, other: _CmpT, /) -> bool: ...

class _ComparableLessThan(Protocol[_CmpT]):
    def __lt__(self, other: _CmpT, /) -> bool: ...

class _ComparableLessThanOrEqual(Protocol[_CmpT]):
    def __le__(self, other: _CmpT, /) -> bool: ...

class CheckType(_BaseCheck):
    # Helper functions exposed as attributes on the check object
    assert_equal: Callable[..., None]
    equal: Callable[..., bool]
    not_equal: Callable[..., bool]
    is_: Callable[..., bool]
    is_not: Callable[..., bool]
    is_true: Callable[..., bool]
    is_false: Callable[..., bool]
    is_none: Callable[..., bool]
    is_not_none: Callable[..., bool]
    is_nan: Callable[..., bool]
    is_not_nan: Callable[..., bool]
    is_in: Callable[..., bool]
    is_not_in: Callable[..., bool]
    is_instance: Callable[..., bool]
    is_not_instance: Callable[..., bool]
    almost_equal: Callable[..., bool]
    not_almost_equal: Callable[..., bool]
    @overload
    def greater(self, a: float, b: float, msg: str = "") -> bool: ...
    @overload
    def greater(
        self,
        a: SupportsFloat | SupportsIndex,
        b: SupportsFloat | SupportsIndex,
        msg: str = "",
    ) -> bool: ...
    @overload
    def greater(
        self, a: _ComparableGreaterThan[_CmpT], b: _CmpT, msg: str = ""
    ) -> bool: ...
    @overload
    def greater_equal(self, a: float, b: float, msg: str = "") -> bool: ...
    @overload
    def greater_equal(
        self,
        a: SupportsFloat | SupportsIndex,
        b: SupportsFloat | SupportsIndex,
        msg: str = "",
    ) -> bool: ...
    @overload
    def greater_equal(
        self, a: _ComparableGreaterThanOrEqual[_CmpT], b: _CmpT, msg: str = ""
    ) -> bool: ...
    @overload
    def less(self, a: float, b: float, msg: str = "") -> bool: ...
    @overload
    def less(
        self,
        a: SupportsFloat | SupportsIndex,
        b: SupportsFloat | SupportsIndex,
        msg: str = "",
    ) -> bool: ...
    @overload
    def less(self, a: _ComparableLessThan[_CmpT], b: _CmpT, msg: str = "") -> bool: ...
    @overload
    def less_equal(self, a: float, b: float, msg: str = "") -> bool: ...
    @overload
    def less_equal(
        self,
        a: SupportsFloat | SupportsIndex,
        b: SupportsFloat | SupportsIndex,
        msg: str = "",
    ) -> bool: ...
    @overload
    def less_equal(
        self, a: _ComparableLessThanOrEqual[_CmpT], b: _CmpT, msg: str = ""
    ) -> bool: ...
    @overload
    def between(
        self,
        b: float,
        a: float,
        c: float,
        msg: str = "",
        ge: bool = False,
        le: bool = False,
    ) -> bool: ...
    @overload
    def between(
        self,
        b: SupportsFloat | SupportsIndex,
        a: SupportsFloat | SupportsIndex,
        c: SupportsFloat | SupportsIndex,
        msg: str = "",
        ge: bool = False,
        le: bool = False,
    ) -> bool: ...
    @overload
    def between(
        self,
        b: _ComparableLessThanOrEqual[_CmpT],
        a: _CmpT,
        c: _CmpT,
        msg: str = "",
        ge: bool = False,
        le: bool = False,
    ) -> bool: ...
    @overload
    def between_equal(self, b: float, a: float, c: float, msg: str = "") -> bool: ...
    @overload
    def between_equal(
        self,
        b: SupportsFloat | SupportsIndex,
        a: SupportsFloat | SupportsIndex,
        c: SupportsFloat | SupportsIndex,
        msg: str = "",
    ) -> bool: ...
    @overload
    def between_equal(
        self,
        b: _ComparableLessThanOrEqual[_CmpT],
        a: _CmpT,
        c: _CmpT,
        msg: str = "",
    ) -> bool: ...
    check_func: Callable[..., Callable[..., bool]]
    fail: Callable[..., None]

    # Extra helpers attached in __init__.py
    raises: Callable[..., Any]
    any_failures: Callable[..., bool]

    # Some users do check.check, so keep it typed
    check: "CheckType"

check: CheckType

__all__ = [
    # main interface objects
    "check",
    "raises",
    "any_failures",
    # helper functions available as module attributes
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
