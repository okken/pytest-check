from .check_log import log_failure

_stop_on_fail = False


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
