"""A pytest plugin that allows multiple failures per test."""
__version__ = "1.1.0"

import pytest

# allow for top level helper function access:
# import pytest_check
# pytest_check.equal(1, 1)
from pytest_check.check_functions import *  # noqa: F401, F402, F403

# allow for with blocks and assert:
# from pytest_check import check
# with check:
#    assert 1 == 2
from pytest_check.context_manager import check  # noqa: F401, F402, F403

# allow top level raises:
# from pytest_check import raises
# with raises(Exception):
#    raise Exception
# with raises(AssertionError):
#     assert 0
from pytest_check.check_raises import raises  # noqa: F401, F402, F403

# make sure assert rewriting happens
pytest.register_assert_rewrite("pytest_check.check")

# allow for helper functions to be part of check context
# manager and check fixture:
# from pytest_check import check
# def test_():
#     check.equal(1, 1)
#     with check:
#        assert 1 == 2
for func in check_functions.__all__:  # noqa: F405
    setattr(check, func, getattr(check_functions, func))  # noqa: F405
