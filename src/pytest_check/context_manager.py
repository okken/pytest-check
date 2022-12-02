from .check_log import log_failure
from . import check_log

_stop_on_fail = False

# This class has grown into much more than just a context manager.
# it's really the interface into the system.
# TODO: maybe rename it
# TODO: maybe pull in extra funcitonality here instead of in plugin.py


class CheckContextManager(object):
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
                if self.msg is not None:
                    log_failure(f"{self.msg}\n{exc_val}")
                else:
                    log_failure(exc_val)
                self.msg = None
                return True
        self.msg = None

    def __call__(self, msg=None):
        self.msg = msg
        return self

    def set_no_tb(self):
        check_log._no_tb = True

    def set_max_fail(self, x):
        check_log._max_fail = x

    def set_max_report(self, x):
        check_log._max_report = x


check = CheckContextManager()
