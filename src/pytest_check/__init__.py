import pytest

# We need register rewrites before import
pytest.register_assert_rewrite("pytest_check.check_functions") 

from . import check_functions # noqa: E402

# allow for top level helper function access:
# import pytest_check
# pytest_check.equal(1, 1)
from .check_functions import *  # noqa: F401, F402, F403, E402

# allow to know if any_failures due to any previous check
from .check_log import any_failures  # noqa: F401, F402, F403, E402

# allow top level raises:
# from pytest_check import raises
# with raises(Exception):
#    raise Exception
# with raises(AssertionError):
#     assert 0
from .check_raises import raises  # noqa: F401, F402, F403, E402

# allow for with blocks and assert:
# from pytest_check import check
# with check:
#    assert 1 == 2
from .context_manager import check  # noqa: F401, F402, F403, E402

# allow check.raises()
setattr(check, "raises", raises)

# allow check.any_failures()
setattr(check, "any_failures", any_failures)

# allow check.check as a context manager.
# weird, but some people are doing it.
# deprecate this eventually
setattr(check, "check", check)

# allow for helper functions to be part of check context
# manager and check fixture:
# from pytest_check import check
# def test_():
#     check.equal(1, 1)
#     with check:
#        assert 1 == 2
for func in check_functions.__all__:  # noqa: F405
    setattr(check, func, getattr(check_functions, func))  # noqa: F405

__all__ = ["raises", "any_failures"]