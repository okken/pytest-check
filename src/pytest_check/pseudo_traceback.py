import inspect
import os
import re
from pprint import pformat

_traceback_style = "auto"


def get_full_context(frame):
    (_, filename, line, funcname, contextlist) = frame[0:5]
    locals = frame.frame.f_locals
    tb_hide = locals.get("__tracebackhide__", False)
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
    return (filename, line, funcname, context, locals, tb_hide)

COLOR_RED = "\x1b[31m"
COLOR_RESET = "\x1b[0m"

def reformat_raw_traceback(lines, color):
    formatted = []
    for line in lines:
        if 'Traceback (most recent call last)' in line:
            continue
        if 'AssertionError' in line:
            if color:
                line = f"{COLOR_RED}{line}{COLOR_RESET}"
            formatted.append(line)
            continue
        result = re.search(r'File "(.*)", line (.*), in (\w*)$\n\W*(.*)',
                           line, flags=re.MULTILINE)
        if result:
            file_path, line_no, func_name, context = result.groups()
            file_name = os.path.basename(file_path)
            if color:
                file_name = f"{COLOR_RED}{file_name}{COLOR_RESET}"
            #formatted.append(f'{file_name}:{line_no} in {func_name}\n    {context}')
            formatted.append(f'{file_name}:{line_no} in {func_name} -> {context}')
        else:
            # I don't have a test case to hit this clause yet
            # And I can't think of one.
            # But it feels weird to not have the if/else.
            # Thus the "no cover"
            formatted.append(line)  # pragma: no cover
    return '\n'.join(formatted)


def _build_pseudo_trace_str(showlocals, tb, color):
    """
    built traceback styles for better error message
    only supports no
    """
    if _traceback_style == "no":
        return ""

    skip_own_frames = 3
    pseudo_trace = []
    func = ""

    if tb:
        pseudo_trace.append(reformat_raw_traceback(tb, color))

    context_stack = inspect.stack()[skip_own_frames:]
    while "test_" not in func and context_stack:
        full_context =  get_full_context(context_stack.pop(0))
        (file, line, func, context, locals, tb_hide) = full_context
        # we want to trace through user code, not 3rd party or builtin libs
        if "site-packages" in file:
            break
        # if called outside of a test, we might hit this
        if "<module>" in func:
            break
        if tb_hide:
            continue
        if showlocals:
            for name, val in reversed(locals.items()):
                if not name.startswith('@py'):
                   pseudo_trace.append("%-10s = %s" % (name, pformat(val,
                                                                     sort_dicts=False,
                                                                     compact=True)))
        file = os.path.basename(file)

        if color:
            file = f"{COLOR_RED}{file}{COLOR_RESET}"
        #line = f"{file}:{line} in {func}\n    {context}"
        line = f"{file}:{line} in {func}() -> {context}"
        pseudo_trace.append(line)

    return "\n".join(reversed(pseudo_trace)) + "\n"
