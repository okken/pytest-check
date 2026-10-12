import pytest


def test_locals_context_manager(pytester):
    pytester.copy_example("examples/test_example_locals.py")
    result = pytester.runpytest("test_example_locals.py::test_ctx", "-l")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines([
        "*a *= 1*",
        "*b *= 2*"
    ])


@pytest.mark.parametrize("verbosity", [[], ["-v"], ["-vv"]])
@pytest.mark.parametrize("check_style", ["function", "context"])
def test_long_locals_follow_verbosity(pytester, verbosity, check_style):
    failure = (
        "check.equal(1, 2)"
        if check_style == "function"
        else "with check:\n        assert 1 == 2"
    )
    pytester.makepyfile(
        f"""
from pytest_check import check

def test_long_local():
    payload = list(range(4000))
    {failure}
"""
    )
    result = pytester.runpytest("-l", "--color=no", *verbosity)
    result.assert_outcomes(failed=1)
    output = result.stdout.str()
    assert "payload" in output
    if verbosity == ["-vv"]:
        assert "3999" in output
    else:
        assert "3999" not in output
        assert "..." in output


def test_locals_check_function(pytester):
    pytester.copy_example("examples/test_example_locals.py")
    result = pytester.runpytest("test_example_locals.py::test_check_func",
                                "--showlocals")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines([
        "*a *= 1*",
        "*b *= 2*"
    ])
