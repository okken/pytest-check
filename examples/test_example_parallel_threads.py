"""
pytest-run-parallel demo

Run this example with pytest-run-parallel installed:

    pip install pytest-run-parallel
    pytest examples/test_example_parallel_threads.py --parallel-threads=4 -v

pytest-run-parallel runs a single test's body concurrently in several
threads rather than running separate tests, so pytest-check's own
"Failed Checks: N" reporting for the test as a whole is a combined total
across every thread - true before and after the fix. The property this
example actually checks is per-thread: each thread should see only the
failures *it* logged via check_log.get_failures(), not its siblings'.

That per-thread result is printed (not asserted) because pytest-check's
own test reporting replaces a test's failure output whenever real check
failures occur, which would otherwise hide a plain assert's message.
Instead, look for a "MISMATCH" line in the captured stdout: its absence
means every thread's check failures were tracked independently.

Without --parallel-threads (or without the plugin installed), the test
runs single-threaded with thread_index == 0 and num_failures == 0, so no
checks are logged and there's nothing to print.
"""

import threading

from pytest_check import check, check_log

_barrier_lock = threading.Lock()
_barrier = None


def _get_barrier(num_parallel_threads):
    # Built lazily (rather than at import time) because its size depends on
    # the --parallel-threads value, which pytest-run-parallel only exposes
    # via this fixture. Guarded by a lock since multiple threads could
    # otherwise race to create it.
    global _barrier
    with _barrier_lock:
        if _barrier is None:
            _barrier = threading.Barrier(num_parallel_threads)
    return _barrier


def test_check_failures_leak_across_parallel_threads(thread_index, num_parallel_threads):
    barrier = _get_barrier(num_parallel_threads)

    # Each parallel thread logs a different, known number of failures.
    num_failures = thread_index

    barrier.wait()  # make sure every thread starts logging at the same time
    for _ in range(num_failures):
        check.equal(1, 2)
    barrier.wait()  # make sure every thread finishes logging before any reads the count

    seen = len(check_log.get_failures())
    if seen == num_failures:
        print(f"thread {thread_index}: saw its own {seen} failure(s), as expected")
    else:
        print(
            f"MISMATCH: thread {thread_index} expected to see {num_failures} of "
            f"its own failures, but check_log reports {seen} total failures"
        )

