from tests.markers import require_pytest_freethreaded, require_pytest_swarm


@require_pytest_swarm
def test_check_failures_are_isolated_across_pytest_swarm_items(pytester):
    pytester.makepyfile(
        """
        import pytest

        from pytest_check import check


        @pytest.mark.swarm(max_workers=4)
        @pytest.mark.parametrize("num_failures", [0, 1, 2, 3])
        def test_parallel_item_failures_are_isolated(num_failures):
            for _ in range(num_failures):
                check.equal(1, 2)
        """
    )

    result = pytester.runpytest("--swarm-workers=4", "-v")

    result.assert_outcomes(passed=1, failed=3)
    output = str(result.stdout)
    for count in (1, 2, 3):
        assert f"Failed Checks: {count}" in output


@require_pytest_freethreaded
def test_check_failures_are_isolated_across_pytest_freethreaded_workers(pytester):
    pytester.makepyfile(
        """
        import threading

        import pytest

        from pytest_check import check, check_log


        barrier = threading.Barrier(4, timeout=10)
        main_thread = threading.get_ident()


        @pytest.mark.freethreaded(threads=4, iterations=4)
        def test_parallel_calls_keep_independent_check_state():
            if threading.get_ident() == main_thread:
                # pytest runs the ordinary call once after the plugin's
                # worker calls complete; it is not part of their barrier.
                check.equal(1, 2)
                return

            barrier.wait()
            check.equal(1, 2)
            barrier.wait()
            seen = check_log.get_num_failures()
            if seen != 1:
                print(
                    f"MISMATCH: expected this worker to see 1 failure, got {seen}"
                )
        """
    )

    result = pytester.runpytest("-v")

    result.assert_outcomes(failed=1)
    # The plugin runs four worker calls and pytest then invokes the test
    # once more in the main thread after its hook returns.
    result.stdout.fnmatch_lines(["*Failed Checks: 5*"])
    result.stdout.no_fnmatch_line("*MISMATCH*")
