from __future__ import annotations
import contextvars
import threading
from collections.abc import Iterable
from typing import Callable

from .pseudo_traceback import _build_pseudo_trace_str, _build_single_line_trace_str

should_use_color: bool = False
COLOR_RED = "\x1b[31m"
COLOR_RESET = "\x1b[0m"
_stop_on_fail = False

# Session-wide config, set once in pytest_configure() before any test runs.
# Safe to keep as plain globals - never mutated per-test.
_default_max_fail = None
_default_max_report = None
_default_max_tb: int = 1
_default_max_tb_line: int | None = None

_showlocals: bool = False


class _CheckState:
    """Failure bookkeeping for a single, currently-running test, or for a
    single thread spawned from one (see _propagate_context_to_new_threads).

    Each state tracks its own failures only, and keeps a list of any child
    states registered by threads spawned while it was current. The
    all_*() methods walk that tree to answer "how many failures happened
    in this test, including every thread it (transitively) spawned?",
    while a thread reading its own state directly (via get_failures() from
    inside that thread) sees only the failures it logged itself.
    """

    def __init__(self) -> None:
        self.failures: list[str] = []
        self.num_failures = 0
        self.max_fail: int | None = _default_max_fail
        self.max_report: int | None = _default_max_report
        self.max_tb: int = _default_max_tb
        self.max_tb_line: int | None = _default_max_tb_line
        self.fail_function: Callable[[str], None] | None = None
        # Track checks with xfail reasons
        self.xfailed_failure: str | None = None
        self._children: list[_CheckState] = []
        # Guards _children: multiple sibling threads may spawn further
        # threads of their own concurrently.
        self._children_lock = threading.Lock()

    def new_child(self) -> _CheckState:
        """Create a state for a newly spawned thread, inheriting this
        state's config (max_fail, fail_function, ...), and register it so
        this state's all_*() methods pick up its failures too.
        """
        child = _CheckState()
        child.max_fail = self.max_fail
        child.max_report = self.max_report
        child.max_tb = self.max_tb
        child.max_tb_line = self.max_tb_line
        child.fail_function = self.fail_function
        with self._children_lock:
            self._children.append(child)
        return child

    def _snapshot_children(self) -> list[_CheckState]:
        with self._children_lock:
            return list(self._children)

    def all_failures(self) -> list[str]:
        failures = list(self.failures)
        for child in self._snapshot_children():
            failures.extend(child.all_failures())
        return failures

    def all_num_failures(self) -> int:
        total = self.num_failures
        for child in self._snapshot_children():
            total += child.all_num_failures()
        return total

    def all_xfailed_failure(self) -> str | None:
        if self.xfailed_failure is not None:
            return self.xfailed_failure
        for child in self._snapshot_children():
            found = child.all_xfailed_failure()
            if found is not None:
                return found
        return None


# One _CheckState tree per *currently executing test*, rooted at whichever
# state was bound when the real pytest test item's call phase began.
#
# A plain threading.local() would isolate state between OS threads, which is
# exactly what's needed when a thread-based parallel runner (pytest-swarm,
# pytest-run-parallel, pytest-freethreaded, ...) executes several *different*
# tests concurrently in separate worker threads - each worker must get its
# own failure list.
#
# But pytest-check also documents and tests a different pattern: a *single*
# test spawning helper threads (via threading.Thread or ThreadPoolExecutor)
# and expecting check failures raised inside them to count against that one
# test (see tests/test_thread.py). A bare threading.local() breaks that,
# because the helper thread would get its own empty state that the main
# thread's test report never sees.
#
# _CheckState's parent/child tree reconciles both: every new OS thread gets
# its own, private _CheckState (so each thread can answer "how many of
# *these* failures are mine?" correctly), but that state is also registered
# as a child of whichever state was current in the thread that spawned it.
# Reading failures via the all_*() methods walks the whole tree, so the
# thread (or real test) at the root of the tree still sees every failure
# logged by every thread it transitively spawned - preserving the "helper
# thread's checks belong to the test that spawned it" behaviour that
# pytest-check's global-state implementation used to provide for free.
_state_var: contextvars.ContextVar[_CheckState] = contextvars.ContextVar(
    "pytest_check_state"
)


def _current_state() -> _CheckState:
    try:
        return _state_var.get()
    except LookupError:
        state = _CheckState()
        _state_var.set(state)
        return state


_propagation_installed = False


def _propagate_context_to_new_threads() -> None:
    """Give new threads their own _CheckState, registered as a child of
    whichever state is current in the spawning thread.

    threading.Thread (and, transitively, ThreadPoolExecutor workers on their
    first task) normally start with a fresh, empty Context, so a ContextVar
    set in the parent thread would not be visible to code running in the
    child thread. Patching Thread.start() to bind a freshly-created child
    _CheckState - parented to the spawning thread's current state - into a
    copy of the calling thread's Context gives the new thread private
    bookkeeping while keeping its failures visible to the spawning thread's
    all_*() queries.

    This is a process-wide, one-time patch applied when pytest-check is
    loaded; it only affects contextvars propagation and has no effect on
    unrelated thread behaviour.
    """
    global _propagation_installed
    if _propagation_installed:
        return
    _propagation_installed = True

    original_start = threading.Thread.start

    def start_with_context(self: threading.Thread) -> None:
        child_state = _current_state().new_child()
        ctx = contextvars.copy_context()
        original_run = self.run

        def run_in_context() -> None:
            def body() -> None:
                _state_var.set(child_state)
                original_run()

            ctx.run(body)

        self.run = run_in_context  # type: ignore[method-assign]  # ty: ignore[invalid-assignment]
        original_start(self)

    threading.Thread.start = start_with_context  # type: ignore[method-assign]


_propagate_context_to_new_threads()


def clear_failures() -> None:
    # gets called at the beginning of each test function
    state = _CheckState()
    state.fail_function = _current_state().fail_function
    _state_var.set(state)


def any_failures() -> bool:
    return bool(get_failures())


def get_failures() -> list[str]:
    return _current_state().all_failures()


def get_num_failures() -> int:
    return _current_state().all_num_failures()


def log_failure(
    msg: object = "",
    check_str: str = "",
    tb: Iterable[str] | None = None,
    xfail: str | None = None,
) -> None:
    __tracebackhide__ = True
    state = _current_state()
    state.num_failures += 1

    msg = str(msg).strip()

    if check_str:
        msg = f"{msg}: {check_str}"

    if (state.max_report is None) or (state.num_failures <= state.max_report):
        if state.num_failures <= state.max_tb:
            pseudo_trace_str = _build_pseudo_trace_str(
                _showlocals, tb, should_use_color
            )
            msg = f"{msg}\n{pseudo_trace_str}"
        elif (
            state.max_tb_line is not None
            and state.num_failures <= state.max_tb_line
        ):
            pseudo_trace_str = _build_single_line_trace_str(tb, should_use_color)
            if pseudo_trace_str:
                msg = f"{msg}, {pseudo_trace_str}"

        if should_use_color:
            msg = f"{COLOR_RED}FAILURE: {COLOR_RESET}{msg}"
        else:
            msg = f"FAILURE: {msg}"
        state.failures.append(msg)

        if xfail and state.xfailed_failure is None:
            state.xfailed_failure = xfail

        if state.fail_function:
            state.fail_function(str(msg))

    if state.max_fail and (state.num_failures >= state.max_fail):
        assert_msg = f"pytest-check max fail of {state.num_failures} reached"
        assert state.num_failures < state.max_fail, assert_msg

    if _stop_on_fail:
        assert False, "Stopping on first failure"


def get_xfailed_failure() -> str | None:
    """Return the xfail reason for the first check that failed with xfail."""
    return _current_state().all_xfailed_failure()
