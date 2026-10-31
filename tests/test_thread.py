import gc
import threading
from threading import Barrier, Thread, Timer
import weakref

import pytest

from pytest_check import check, check_log


@pytest.mark.parametrize("timer", [False, True])
def test_finished_threads_do_not_need_garbage_collection(timer):
    was_enabled = gc.isenabled()
    gc.disable()
    try:
        thread = Timer(60, lambda: None) if timer else Thread(target=lambda: None)
        reference = weakref.ref(thread)
        thread.start()
        if isinstance(thread, Timer):
            thread.cancel()
        thread.join()
        del thread
        assert reference() is None
    finally:
        if was_enabled:
            gc.enable()


def test_thread_run_override_is_restored():
    thread = Thread()

    def original_run():
        pass
    thread.__dict__["run"] = original_run
    thread.start()
    thread.join()
    assert thread.run is original_run


def test_failed_thread_start_does_not_leave_wrapper():
    thread = Thread(target=lambda: None)
    thread.start()
    thread.join()
    with pytest.raises(RuntimeError, match="once"):
        thread.start()
    assert "run" not in thread.__dict__


def test_thread_run_is_restored_after_error(monkeypatch):
    errors = []
    monkeypatch.setattr(threading, "excepthook", lambda args: errors.append(args.exc_type))

    def fail():
        raise ValueError("thread failed")

    thread = Thread(target=fail)
    thread.start()
    thread.join()
    assert errors == [ValueError]
    assert "run" not in thread.__dict__


def test_failing_threaded_testcode(pytester):
    pytester.copy_example("examples/test_example_fail_in_thread.py")
    result = pytester.runpytest()
    result.assert_outcomes(failed=2, passed=0)
    result.stdout.fnmatch_lines(["*1 + 1 is 2, not 3*"])
    result.stdout.fnmatch_lines(["*1 + 1 is 2, not 4*"])


def test_passing_threaded_testcode(pytester):
    pytester.copy_example("examples/test_example_pass_in_thread.py")
    result = pytester.runpytest()
    result.assert_outcomes(failed=0, passed=2)


def test_xfailed_state_is_aggregated_from_child_thread():
    # The test report reads the root state, which must include xfail reasons
    # recorded by helper threads as well as failures recorded by the root.
    parent = check_log._CheckState()
    child = parent.new_child()

    child.xfailed_failure = "failure in child thread"

    assert parent.all_xfailed_failure() == "failure in child thread"


def test_thread_context_propagation_is_idempotent():
    # check_log installs the Thread.start() wrapper when imported. Calling the
    # installer again must not wrap Thread.start() repeatedly.
    check_log._propagate_context_to_new_threads()


def test_concurrent_check_failures_are_tracked_per_thread():
    """
    Each thread's check failures should be tracked independently, so
    that concurrent threads (standing in for separate tests run by a
    thread-based parallel runner, e.g. pytest-run-parallel) never see each
    other's failures. Two threads each log a different, known number of
    failures at the same time; each should see only its own count.
    test_parallel_threads.py demonstrates this behavior also, but requires
    the pytest-run-parallel plugin to run tests concurrently in multiple threads.
    Having this test ensures that even without the pytest-run-parallel plugin,
    the per-thread isolation of check failures is verified.
    """
    # Barriers force both threads to log failures at the same time, so the
    # race is hit reliably instead of depending on scheduling luck.
    start_checks = Barrier(2)
    finish_checks = Barrier(2)

    # Threads don't have return values, so collect results here instead,
    # keyed by each thread's own failure count.
    observed_failures = {}

    def run_checks(num_failures):
        check_log.clear_failures()  # normally done once per test
        start_checks.wait()  # wait for the other thread to be ready
        for _ in range(num_failures):
            check.equal(1, 2)  # always fails, so this logs num_failures failures
        finish_checks.wait()  # wait for the other thread to finish logging
        observed_failures[num_failures] = len(check_log.get_failures())

    threads = [Thread(target=run_checks, args=(count,)) for count in (3, 5)]
    try:
        for thread in threads:
            thread.start()  # schedules run_checks() to run concurrently
        for thread in threads:
            thread.join()  # wait for both threads to finish before asserting
        # Isolated per-thread state would give {3: 3, 5: 5}; shared global
        # state instead lets both threads see each other's failures too.
        assert observed_failures == {3: 3, 5: 5}
    finally:
        check_log.clear_failures()
