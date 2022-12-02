def test_baseline(pytester):
    pytester.copy_example("examples/test_example_multiple_failures.py")
    result = pytester.runpytest()
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: * 7 == 100",
            "*test_multiple_failures() -> check.equal(i, 100)",
            "*FAILURE: * 8 == 100",
            "*test_multiple_failures() -> check.equal(i, 100)",
            "*FAILURE: * 9 == 100",
            "*test_multiple_failures() -> check.equal(i, 100)",
            "Failed Checks: 10",
        ]
    )


def test_no_tb(pytester):
    pytester.copy_example("examples/test_example_multiple_failures.py")
    result = pytester.runpytest("--check-no-tb")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: * 7 == 100",
            "*FAILURE: * 8 == 100",
            "*FAILURE: * 9 == 100",
            "Failed Checks: 10",
        ]
    )
    result.stdout.no_fnmatch_line("*test_multiple_failures() -> check.equal(i, 100)")


def test_max_report(pytester):
    pytester.copy_example("examples/test_example_multiple_failures.py")
    result = pytester.runpytest("--check-max-report=5")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: * 1 == 100",
            "*FAILURE: * 2 == 100",
            "*FAILURE: * 3 == 100",
            "*FAILURE: * 4 == 100",
            "*FAILURE: * 5 == 100",
            "Failed Checks: 10",
        ]
    )
    result.stdout.no_fnmatch_line("*FAILURE: * 6 == 100")


def test_max_fail(pytester):
    pytester.copy_example("examples/test_example_multiple_failures.py")
    result = pytester.runpytest("--check-max-fail=5")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: * 1 == 100",
            "*FAILURE: * 2 == 100",
            "*FAILURE: * 3 == 100",
            "*FAILURE: * 4 == 100",
            "*FAILURE: * 5 == 100",
            "Failed Checks: 5",
            "*AssertionError: pytest-check max fail of 5 reached",
        ]
    )
    result.stdout.no_fnmatch_line("*FAILURE: * 6 == 100")
