from threading import Barrier, Thread

from pytest_check import check, check_log


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
