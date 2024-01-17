def test_fail_func(pytester):
    pytester.copy_example("examples/test_example_fail_func.py")
    result = pytester.runpytest("--check-max-tb=2")
    result.assert_outcomes(failed=2)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: one",
            "*test_one_failure() -> check.fail('one')",
            "Failed Checks: 1",
            "*FAILURE: one",
            "*test_two_failures() -> check.fail('one')",
            "*FAILURE: two",
            "*test_two_failures() -> check.fail('two')",
            "Failed Checks: 2",
        ],
    )
