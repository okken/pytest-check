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

    # pytest-run-parallel runs the test body concurrently in 4 threads.
    # If check_log's state were thread-local, each thread would only see
    # its own failures and the whole run would still pass. 
    result = pytester.runpytest("--parallel-threads=4")
    result.assert_outcomes(passed=1)
