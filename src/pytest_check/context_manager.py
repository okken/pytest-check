import warnings
import traceback
from . import check_log
from .check_log import log_failure

_stop_on_fail = False

# This class has grown into much more than just a context manager.
# it's really the interface into the system.
# TODO: maybe rename it
# TODO: maybe pull in extra functionality here instead of in plugin.py


class CheckContextManager:
    def __init__(self):
        self.msg = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        __tracebackhide__ = True
        if exc_type is not None and issubclass(exc_type, AssertionError):
            if _stop_on_fail:
                self.msg = None
                return
            else:
                fmt_tb = traceback.format_exception(exc_type, exc_val, exc_tb)
                if self.msg is not None:
                    log_failure(f"{exc_val}, {self.msg}", tb=fmt_tb)
                else:
                    log_failure(exc_val, tb=fmt_tb)
                self.msg = None
                return True
        self.msg = None

    def __call__(self, msg=None):
        self.msg = msg
        return self

    def set_no_tb(self):
        warnings.warn(
            "set_no_tb() is deprecated; use set_max_tb(0)", DeprecationWarning
            )
        check_log._max_tb = 0

    def set_max_fail(self, x):
        check_log._max_fail = x

    def set_max_report(self, x):
        check_log._max_report = x

    def set_max_tb(self, x):
        check_log._max_tb = x

    def call_on_fail(self, func):
        """Experimental feature - may change with any release"""
        check_log._fail_function = func


check = CheckContextManager()
