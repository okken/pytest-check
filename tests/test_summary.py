import pytest


require_pytest_7_3 = pytest.mark.skipif(
    pytest.version_tuple < (7, 3, 0),
    reason="summary message only supported on pytest7.3+")


@require_pytest_7_3
def test_baseline(pytester):
    pytester.copy_example("examples/test_example_summary.py")
    result = pytester.runpytest("-k check_no_msg")
    result.stdout.fnmatch_lines(["*FAILED*-*check 1 == 2*"])


@require_pytest_7_3
def test_message(pytester):
    pytester.copy_example("examples/test_example_summary.py")
    result = pytester.runpytest("-k check_msg")
    result.stdout.fnmatch_lines(["*FAILED*-*check 1 == 2*comment about*"])
