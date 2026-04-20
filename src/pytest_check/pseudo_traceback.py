from __future__ import annotations
import inspect
import os
import re
import sys
from collections.abc import Iterable
from inspect import FrameInfo
from pprint import pformat
from typing import AnyStr, Any

if sys.version_info < (3, 11):  # pragma: no cover
    from typing_extensions import LiteralString
else:
    from typing import LiteralString


_traceback_style = "auto"


def get_full_context(
    frame: FrameInfo,
) -> tuple[AnyStr | LiteralString | str, int, str, str, dict[str, Any], bool]:
    (_, filename, line, funcname, contextlist) = frame[0:5]
    locals_ = frame.frame.f_locals
    tb_hide = bool(locals_.get("__tracebackhide__", False))
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
    return filename, line, funcname, context, locals_, tb_hide


COLOR_RED = "\x1b[31m"
COLOR_RESET = "\x1b[0m"


def reformat_raw_traceback(lines: Iterable[str], color: bool) -> str:
    formatted: list[str] = []
    for line in lines:
        if "Traceback (most recent call last)" in line:
            continue
        if "AssertionError" in line:
            if color:
                line = f"{COLOR_RED}{line}{COLOR_RESET}"
            formatted.append(line)
            continue
        result = re.search(
            r'File "(.*)", line (.*), in (\w*)$\n\W*(.*)', line, flags=re.MULTILINE
        )
        if result:
            file_path, line_no, func_name, context = result.groups()
            file_name = os.path.basename(file_path)
            if color:
                file_name = f"{COLOR_RED}{file_name}{COLOR_RESET}"
            # formatted.append(f'{file_name}:{line_no} in {func_name}\n    {context}')
            formatted.append(f"{file_name}:{line_no} in {func_name} -> {context}")
        else:
            # I don't have a test case to hit this clause yet
            # And I can't think of one.
            # But it feels weird to not have the if/else.
            # Thus, the "no cover"
            formatted.append(line)  # pragma: no cover
    return "\n".join(formatted)


def _line_to_trace_frame(
    line: str,
) -> tuple[str, int, str, str] | None:
    result = re.search(
        r'File "(.*)", line (.*), in (\w*)$\n\W*(.*)', line, flags=re.MULTILINE
    )
    if not result:
        return None

    file_path, line_no, func_name, context = result.groups()
    try:
        line_number = int(line_no)
    except ValueError:  # pragma: no cover
        return None

    try:
        file_name = os.path.relpath(file_path)
    except ValueError:  # pragma: no cover
        file_name = os.path.abspath(file_path)  # pragma: no cover

    return file_name, line_number, func_name, context.strip()


def _is_user_trace_frame(file_name: str, func_name: str) -> bool:
    if "site-packages" in file_name or "dist-packages" in file_name:
        return False
    if "src/pytest_check/" in file_name:
        return False
    if "<module>" in func_name:
        return False
    return True


def _extract_exception_summary(tb_lines: list[str]) -> str:
    for raw_line in reversed(tb_lines):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("Traceback (most recent call last)"):
            continue
        if line.startswith("File "):
            continue

        match = re.match(r"^([A-Za-z_][A-Za-z0-9_.]*)(?::\s*(.*))?$", line)
        if not match:
            continue

        exc_type, exc_msg = match.groups()
        if exc_msg:
            return f"{exc_type}: {exc_msg}"
        return exc_type

    return ""


def _build_single_line_trace_str(tb: Iterable[str] | None, color: bool) -> str:
    """
    Build a single line traceback showing the first frame outside pytest-check code.
    Returns: "file:line in func -> context" or empty string if no frames found.
    """
    if _traceback_style == "no":
        return ""

    if tb:
        tb_lines = list(tb)
        tb_frames = []
        for line in tb_lines:
            frame = _line_to_trace_frame(line)
            if frame:
                tb_frames.append(frame)

        exception_summary = _extract_exception_summary(tb_lines)

        # Use the innermost user frame from the exception traceback.
        # This is especially helpful for `with check:` blocks where the
        # relevant line is usually the failing line inside the block.
        for file_name, line_no, func_name, context in reversed(tb_frames):
            if not _is_user_trace_frame(file_name, func_name):
                continue
            if color:
                file_name = f"{COLOR_RED}{file_name}{COLOR_RESET}"
            line_report = f"{file_name}:{line_no} in {func_name}() -> {context}"
            if exception_summary:
                return f"{line_report}: {exception_summary}"
            return line_report

    skip_own_frames = 3
    func = ""

    context_stack = inspect.stack()[skip_own_frames:]
    while "test_" not in func and context_stack:
        full_context = get_full_context(context_stack.pop(0))
        (file, line, func, context, locals, tb_hide) = full_context
        if not _is_user_trace_frame(file, func):
            break
        if tb_hide:
            continue
        # Return the first non-hidden frame
        if color:
            file = f"{COLOR_RED}{file}{COLOR_RESET}"
        return f"{file}:{line} in {func}() -> {context}"

    return ""


def _build_pseudo_trace_str(
    showlocals: bool, tb: Iterable[str] | None, color: bool
) -> str:
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
        full_context = get_full_context(context_stack.pop(0))
        (file, line, func, context, locals, tb_hide) = full_context
        # we want to trace through user code, not 3rd party or builtin libs
        if "site-packages" in file or "dist-packages" in file:
            break
        # if called outside a test, we might hit this
        if "<module>" in func:
            break
        if tb_hide:
            continue
        if showlocals:
            for name, val in reversed(locals.items()):
                if not name.startswith("@py"):
                    pseudo_trace.append(
                        "%-10s = %s"
                        % (name, pformat(val, sort_dicts=False, compact=True))
                    )

        if color:
            file = f"{COLOR_RED}{file}{COLOR_RESET}"
        line_report = f"{file}:{line} in {func}() -> {context}"
        pseudo_trace.append(line_report)

    return "\n".join(reversed(pseudo_trace)) + "\n"
