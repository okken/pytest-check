import inspect
import os

_traceback_style = "auto"


def get_full_context(level):
    (_, filename, line, funcname, contextlist) = inspect.stack()[level][0:5]
    try:
        filename = os.path.relpath(filename)
    except ValueError:  # pragma: no cover
        # this is necessary if we're tracing to a different drive letter
        # such as C: to D:
        #
        # Turning off coverage for abspath, for now,
        # since that path requires testing with an odd setup.
        # But.... we'll keep looking for a way to test it. :)
        filename = os.path.abspath(filename)  # pragma: no cover
    context = contextlist[0].strip() if contextlist else ""
    return (filename, line, funcname, context)


def _build_pseudo_trace_str():
    """
    built traceback styles for better error message
    only supports no
    """
    if _traceback_style == "no":
        return ""

    level = 4
    pseudo_trace = []
    func = ""
    while "test_" not in func:
        (file, line, func, context) = get_full_context(level)
        # we want to trace through user code, not 3rd party or builtin libs
        if "site-packages" in file:
            break
        # if called outside of a test, we might hit this
        if "<module>" in func:
            break
        line = "{}:{} in {}() -> {}".format(file, line, func, context)
        pseudo_trace.append(line)
        level += 1

    return "\n".join(reversed(pseudo_trace)) + "\n"
