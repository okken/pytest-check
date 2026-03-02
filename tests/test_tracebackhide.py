import inspect
import sys
import pytest


@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python3.10 or higher")
@pytest.mark.parametrize("filename", ["site-packages/foo.py", "dist-packages/bar.py"])
def test_3rd_party_traceback(pytester, monkeypatch, filename):
    original_inspect_stack = inspect.stack

    def inspect_stack_wrapper(context=1):
        # call the original API and ignore this wrapper frame
        frames = original_inspect_stack(context)[1:]

        # insert a dummy frame pointing to 3rd party code before the failed check
        # (the first 3 frames belong to pytest-check)
        frames.insert(3, inspect.FrameInfo(frames[0].frame, filename, 0, "", None, None))

        return frames

    monkeypatch.setattr("inspect.stack", inspect_stack_wrapper)

    pytester.copy_example("examples/test_example_helpers.py")
    result = pytester.runpytest("--check-max-tb=2")
    result.assert_outcomes(failed=1, passed=0)

    result.stdout.no_fnmatch_line(f"{filename}*")
    result.stdout.no_fnmatch_line("*in test_func() -> helper1()")
    result.stdout.no_fnmatch_line("*in helper1() -> helper2()")

    result.stdout.fnmatch_lines(
        [
            "*FAILURE: assert 1 == 0, first",
            "*in helper2 -> assert 1 == 0",
            "*AssertionError: assert 1 == 0",

            "*FAILURE: assert 1 > 2, second",
            "*in helper2 -> assert 1 > 2",
            "*AssertionError: assert 1 > 2",
            "*Failed Checks: 2*",
        ],
    )

@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python3.10 or higher")
def test_normal_pseudo_traceback(pytester):
    """
    Should show a sequence of calls
    """
    pytester.copy_example("examples/test_example_helpers.py")
    result = pytester.runpytest("--check-max-tb=2")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: assert 1 == 0, first",
            "*in test_func() -> helper1()",
            "*in helper1() -> helper2()",
            "*in helper2 -> assert 1 == 0",
            "*AssertionError: assert 1 == 0",

            "*FAILURE: assert 1 > 2, second",
            "*in test_func() -> helper1()",
            "*in helper1() -> helper2()",
            "*in helper2 -> assert 1 > 2",
            "*AssertionError: assert 1 > 2",
            "*Failed Checks: 2*",
        ],
    )

@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python3.10 or higher")
def test_tracebackhide(pytester):
    """
    Should skip helper1, since it has __tracebackhide__ = True
    """
    pytester.copy_example("examples/test_example_tracebackhide.py")
    result = pytester.runpytest("--check-max-tb=2")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.no_fnmatch_line("*in helper1() -> helper2()")

