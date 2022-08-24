def test_sequence_with_helper_funcs(pytester):
    """
    Should show a sequence of calls
    """
    pytester.copy_example("examples/test_example_helpers.py")
    result = pytester.runpytest()
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: first",
            "*in test_func() -> helper1()",
            "*in helper1() -> helper2()",
            '*in helper2() -> with check("first"): assert 1 == 0',
            "*FAILURE: second",
            "*in test_func() -> helper1()",
            "*in helper1() -> helper2()",
            '*in helper2() -> with check("second"): assert 1 > 2',
            "*Failed Checks: 2*",
        ]
    )
