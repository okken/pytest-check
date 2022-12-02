"""
The error caused by our example is on purpose.
However, the import system in some versions of Python (such as 3.7)
don't like it, even when running as a test.

Python 3.10 handles it fine. So that's where we'll test it.
"""
import pytest
import sys


@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python3.10 or higher")
def test_check_not_in_a_test(pytester):
    """
    should error
    """
    pytester.copy_example("examples/test_example_check_not_in_test.py")
    result = pytester.runpytest()
    result.assert_outcomes(errors=1, failed=0, passed=0)
    result.stdout.fnmatch_lines(
        [
            "* ERROR at setup of test_something *",
            "*FAILURE: assert 1 == 0*",
            "*not_in_test.py:* in not_in_a_test() -> helper_func()*",
            "*not_in_test.py:* in helper_func() -> with check:*",
            "*Failed Checks: 1*",
            "* short test summary info *",
            "*ERROR test_example_check_not_in_test.py::test_something*",
        ]
    )
