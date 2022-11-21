"""
Ensure that xfail, both strict and not strict,
behaves correctly for check passes/failures.
"""

from pytest_check import check
import pytest


@pytest.mark.xfail()
def test_xfail():
    "Should xfail"
    check.equal(1, 2)


@pytest.mark.xfail(strict=True)
def test_xfail_strict():
    "Should xfail"
    check.equal(1, 2)


@pytest.mark.xfail()
def test_xfail_pass():
    "Should xpass"
    check.equal(1, 1)


@pytest.mark.xfail(strict=True)
def test_xfail_pass_strict():
    check.equal(1, 1)
