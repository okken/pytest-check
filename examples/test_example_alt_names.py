"""
By default, pytest looks for functions that START with test_
However, it's possible to also look for alternate names, such as
functions ENDING with _test.

To run this example,
- use:
 pytest python_functionspytest
       -o "python_functions=test_* *_test"
       test_example_alt_names.py`

The purpose of this example is to make sure that `check`
works with alternately named tests.
"""
from pytest_check import check


def ends_with_test():
    helper_func()


def test_default_naming():
    pass


def helper_func():
    with check:
        assert 1 == 0
