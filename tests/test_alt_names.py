ini_contents = """
[pytest]
python_functions =
    test_*
    *_test
"""


def test_alt_names(pytester):
    """
    Should stop after first failed check
    """
    pytester.copy_example("examples/test_example_alt_names.py")
    pytester.makeini(ini_contents)
    result = pytester.runpytest()
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: assert 1 == 0*",
            "*_alt_names.py:* in ends_with_test() -> helper_func()*",
            "*_alt_names.py:* in helper_func() -> *",
            "*Failed Checks: 1*",
        ]
    )
    result.assert_outcomes(failed=1, passed=1)
