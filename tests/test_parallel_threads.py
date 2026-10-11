from tests.markers import require_pytest_run_parallel


@require_pytest_run_parallel
def test_check_failures_leak_across_parallel_threads(pytester):
    """
    Test that check failures do not leak across parallel threads.
    This test relies on the pytest-run-parallel plugin to run.
    Another test, test_thread.py, test_concurrent_check_failures_are_tracked_per_thread,
    verifies the same behavior without requiring the pytest-run-parallel plugin.
    """
    pytester.copy_example("examples/test_example_parallel_threads.py")

    # Without real thread-based parallelism, thread_index is always 0 and
    # the example logs no failures - it's a clean, uneventful pass.
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)

    # pytest-run-parallel runs the test body concurrently in 4 threads,
    # each logging a different, known number of failures (0, 1, 2, 3), so
    # the test is expected to fail/error either way - those are genuine
    # check failures (0 + 1 + 2 + 3 = 6), not evidence of the bug.
    #
    # The property under test is per-thread isolation, which each thread
    # prints to stdout rather than asserts (see the example's docstring
    # for why). If check_log's state were shared instead of thread-local,
    # every thread would see all 6 failures instead of just its own, and
    # print a "MISMATCH" line.
    result = pytester.runpytest("--parallel-threads=4")
    result.assert_outcomes(errors=1)
    result.stdout.no_fnmatch_line("*MISMATCH*")

