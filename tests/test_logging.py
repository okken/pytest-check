def test_logging_error_level(pytester):
    """
    Should log 2 failures inside log with error level
    """
    pytester.copy_example("examples/test_example_logging.py")
    result = pytester.runpytest(
        "test_example_logging.py::test_error_level",
        "--logging-level=ERROR",
    )
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(["Failed Checks: 2"])


def test_logging_no_level(pytester):
    """
    Should not log failures
    """
    pytester.copy_example("examples/test_example_logging.py")
    result = pytester.runpytest("test_example_logging.py::test_no_level")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(["Failed Checks: 2"])
