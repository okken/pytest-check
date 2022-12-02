def test_baseline(pytester):
    pytester.copy_example("examples/test_example_message.py")
    result = pytester.runpytest("-k baseline")
    result.stdout.fnmatch_lines(["FAILURE: check 1 == 2"])
    result.stdout.no_fnmatch_line("FAILURE: check 1 == 2: comment about a=1 != b=2")


def test_message(pytester):
    pytester.copy_example("examples/test_example_message.py")
    result = pytester.runpytest("-k message")
    result.stdout.fnmatch_lines(["FAILURE: check 1 == 2: comment about a=1 != b=2"])
