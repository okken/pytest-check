import pytest

pytest.register_assert_rewrite("pytest_check.check")

from pytest_check.check import *  # noqa: F401, F402, F403
