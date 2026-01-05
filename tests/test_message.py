from typing import Callable


def test_check_without_message_shows_default_format(run_example_test: Callable) -> None:
    result = run_example_test("test_example_message.py", "baseline")
    result.stdout.fnmatch_lines(["FAILURE: check 1 == 2"])
    result.stdout.no_fnmatch_line("FAILURE: check 1 == 2: comment about a=1 != b=2")


def test_check_with_message_shows_custom_message(run_example_test: Callable) -> None:
    result = run_example_test("test_example_message.py", "message")
    result.stdout.fnmatch_lines(["FAILURE: check 1 == 2: comment about a=1 != b=2"])
