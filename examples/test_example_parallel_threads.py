"""
pytest-run-parallel demo

Run this example with pytest-run-parallel installed:

    pip install pytest-run-parallel
    pytest examples/test_example_parallel_threads.py --parallel-threads=4 -v

Without --parallel-threads (or without the plugin installed), the test
runs single-threaded with thread_index == 0 and num_failures == 0, so it
passes cleanly - there's no bug to see yet.

With --parallel-threads=4, four threads run the test body concurrently,
each logging a different, known number of failures (0, 1, 2, and 3).
Thread 0 logs none of its own failures and should therefore see 0 - but
because check_log's state is shared, it instead sees all 6 failures
logged by the other three threads, and fails with something like:

    thread 0 expected to see 0 of its own failures, but check_log reports
    6 total failures (state is shared/polluted across threads instead of
    being private per thread)
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
    assert seen == num_failures, (
        f"thread {thread_index} expected to see {num_failures} of its own "
        f"failures, but check_log reports {seen} total failures (state is "
        "shared/polluted across threads instead of being private per thread)"
    )
