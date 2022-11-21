"""
Failures in fixture should result in Error, not Fail.
"""
import pytest
from pytest_check import check


@pytest.fixture()
def a_fixture():
    check.equal(1, 2)


def test_setup_failure(a_fixture):
    pass


@pytest.fixture()
def b_fixture():
    yield
    check.equal(1, 2)


def test_teardown_failure(b_fixture):
    pass
