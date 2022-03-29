"""A pytest plugin that allows multiple failures per test."""
import pytest
from pytest_check.check_methods import *  # noqa: F401, F402, F403

pytest.register_assert_rewrite("pytest_check.check")

__version__ = "1.0.5"
