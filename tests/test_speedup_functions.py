import pytest


def test_baseline(pytester):
    pytester.copy_example("examples/test_example_speedup_funcs.py")
    result = pytester.runpytest("-k baseline", "--check-max-tb=10")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: * 7 == 100",
            "*test_baseline() -> check.equal(i, 100)",
            "*FAILURE: * 8 == 100",
            "*test_baseline() -> check.equal(i, 100)",
            "*FAILURE: * 9 == 100",
            "*test_baseline() -> check.equal(i, 100)",
            "Failed Checks: 10",
        ],
    )


def test_max_report(pytester):
    pytester.copy_example("examples/test_example_speedup_funcs.py")
    result = pytester.runpytest("-k max_report")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: * 1 == 100",
            "*FAILURE: * 2 == 100",
            "*FAILURE: * 3 == 100",
            "*FAILURE: * 4 == 100",
            "*FAILURE: * 5 == 100",
            "Failed Checks: 10",
        ],
    )
    result.stdout.no_fnmatch_line("*FAILURE: * 6 == 100")


def test_max_fail(pytester):
    pytester.copy_example("examples/test_example_speedup_funcs.py")
    result = pytester.runpytest("-k max_fail")
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
        ],
    )
    result.stdout.no_fnmatch_line("*FAILURE: * 6 == 100")


def test_max_tb(pytester):
    pytester.copy_example("examples/test_example_speedup_funcs.py")
    result = pytester.runpytest("-k max_tb", "--show-capture=no")
    result.assert_outcomes(failed=1)
    num_tb = str(result.stdout).count("in test_max_tb() -> check.equal(i, 100)")
    assert num_tb == 2


def test_deprecated_no_tb(check):
    with pytest.deprecated_call():
        check.set_no_tb()


text_for_test_no_tb = """
def test_no_tb(check):
    check.set_no_tb()
    for i in range(1, 11):
        check.equal(i, 100)
"""


def test_no_tb(pytester):
    pytester.makepyfile(text_for_test_no_tb)
    result = pytester.runpytest("-k no_tb")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: * 7 == 100",
            "*FAILURE: * 8 == 100",
            "*FAILURE: * 9 == 100",
            "Failed Checks: 10",
        ],
    )
    result.stdout.no_fnmatch_line("*test_baseline() -> check.equal(i, 100)")
