from __future__ import annotations

from typing import Any, Callable

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
    greater: Callable[..., bool]
    greater_equal: Callable[..., bool]
    less: Callable[..., bool]
    less_equal: Callable[..., bool]
    between: Callable[..., bool]
    between_equal: Callable[..., bool]
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

