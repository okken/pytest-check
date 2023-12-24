def test_baseline(pytester):
    pytester.copy_example("examples/test_example_short_test_summary_info.py")
    result = pytester.runpytest("-k baseline")
    result.stdout.fnmatch_lines(["*FAILED*-*FAILURE*"])


def test_message(pytester):
    pytester.copy_example("examples/test_example_short_test_summary_info.py")
    result = pytester.runpytest("-k message")
    result.stdout.fnmatch_lines(["*FAILED*-*FAILURE*"])
