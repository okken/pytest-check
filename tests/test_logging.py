
# def test_logging_level_error(pytester):
#     """
#     Should log 2 failures inside log with error level
#     """
#     pytester.copy_example("examples/test_example_logging.py")
#     result = pytester.runpytest(
#         "--logging-level=ERROR -k test_logging_error_level"
#     )
#     result.assert_outcomes(failed=1, passed=0)
#     result.stdout.fnmatch_lines(["* 2 failed *"])
#
#
# def test_logging_no_level(pytester):
#     """
#     Should not log failures
#     """
#     pytester.copy_example("examples/test_example_logging.py")
#     result = pytester.runpytest("-k test_logging_no_level")
#     result.assert_outcomes(failed=1, passed=0)
#     result.stdout.fnmatch_lines(["* 2 failed *"])
