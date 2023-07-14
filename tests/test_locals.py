def test_locals_context_manager(pytester):
    pytester.copy_example("examples/test_example_locals.py")
    result = pytester.runpytest("test_example_locals.py::test_ctx", "-l")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines([
        "*a *= 1*",
        "*b *= 2*"
    ])


def test_locals_check_function(pytester):
    pytester.copy_example("examples/test_example_locals.py")
    result = pytester.runpytest("test_example_locals.py::test_check_func",
                                "--showlocals")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines([
        "*a *= 1*",
        "*b *= 2*"
    ])