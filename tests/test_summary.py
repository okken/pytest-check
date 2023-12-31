def test_baseline(pytester):
    pytester.copy_example("examples/test_example_summary.py")
    result = pytester.runpytest("-k check_no_msg")
    result.stdout.fnmatch_lines(["*FAILED*-*check 1 == 2*"])


def test_message(pytester):
    pytester.copy_example("examples/test_example_summary.py")
    result = pytester.runpytest("-k check_msg")
    result.stdout.fnmatch_lines(["*FAILED*-*check 1 == 2*comment about*"])
