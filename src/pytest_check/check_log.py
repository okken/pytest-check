from .pseudo_traceback import _build_pseudo_trace_str

should_use_color = False
COLOR_RED = "\x1b[31m"
COLOR_RESET = "\x1b[0m"
_failures = []
_stop_on_fail = False

_default_max_fail = None
_default_max_report = None
_default_max_tb = None

_max_fail = None
_max_report = None
_max_tb = None
_num_failures = 0
_fail_function = None


def clear_failures():
    # get's called at the beginning of each test function
    global _failures, _num_failures
    global _max_fail, _max_report, _max_tb
    _failures = []
    _num_failures = 0
    _max_fail = _default_max_fail
    _max_report = _default_max_report
    _max_tb = _default_max_tb


def any_failures() -> bool:
    return bool(get_failures())


def get_failures():
    return _failures


def log_failure(msg="", check_str=""):
    global _num_failures
    __tracebackhide__ = True
    _num_failures += 1

    msg = str(msg).strip()

    if check_str:
        msg = f"{msg}: {check_str}"

    if (_max_report is None) or (_num_failures <= _max_report):
        if _num_failures <= _max_tb:
            pseudo_trace_str = _build_pseudo_trace_str()
            msg = f"{msg}\n{pseudo_trace_str}"

        if should_use_color:
            msg = f"{COLOR_RED}{msg}{COLOR_RESET}"

        msg = f"FAILURE: {msg}"
        _failures.append(msg)
        if _fail_function:
            _fail_function(msg)

    if _max_fail and (_num_failures >= _max_fail):
        assert_msg = f"pytest-check max fail of {_num_failures} reached"
        assert _num_failures < _max_fail, assert_msg

    if _stop_on_fail:
        assert False, "Stopping on first failure"
