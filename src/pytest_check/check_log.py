from .pseudo_traceback import _build_pseudo_trace_str
from colorama import Fore

should_use_color = False
_failures = []


def clear_failures():
    global _failures
    _failures = []


def get_failures():
    return _failures


def log_failure(msg=""):
    __tracebackhide__ = True
    pseudo_trace_str = _build_pseudo_trace_str()
    msg_plus_trace = f"{msg}\n{pseudo_trace_str}"
    if should_use_color:
        msg_plus_trace = f"{Fore.RED}{msg_plus_trace}{Fore.RESET}"
    entry = f"FAILURE: {msg_plus_trace}"
    _failures.append(entry)
