"""A pytest plugin that allows multiple failures per test."""
import pytest

pytest.register_assert_rewrite("pytest_check.check")

from pytest_check.check_methods import *  # noqa: F401, F402, F403


__version__ = "0.3.8"
