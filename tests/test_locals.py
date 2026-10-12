import pytest


@pytest.mark.parametrize("check_style", ["function", "context"])
def test_locals(pytester, check_style):
    pytester.copy_example("examples/test_example_locals.py")
    test_func = "test_check_func" if check_style == "function" else "test_ctx"
    result = pytester.runpytest(f"test_example_locals.py::{test_func}", "-l")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines([
        "*a *= 1*",
        "*b *= 2*"
    ])


@pytest.mark.parametrize("verbosity", [[], ["-v"], ["-vv"]], ids=["default", "v", "vv"])
@pytest.mark.parametrize("check_style", ["function", "context"])
def test_long_locals_follow_verbosity(pytester, verbosity, check_style):
    pytester.copy_example("examples/test_example_locals.py")
    test_func = "test_check_func" if check_style == "function" else "test_ctx"
    result = pytester.runpytest(f"test_example_locals.py::{test_func}",
                                "--showlocals", *verbosity)
    result.assert_outcomes(failed=1)
    output = result.stdout.str()
    assert "big_local" in output
    if verbosity == ["-vv"]:
        assert "99" in output
    else:
        assert "99" not in output
        assert "..." in output
