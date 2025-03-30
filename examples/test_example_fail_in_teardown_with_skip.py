"""
Ensure that failing in teardown works.

There's something about this order that can trip up the plugin.

1. A session scope fixture fails in teardown with pytest_check.fail()
2. The last test of the session is skipped.

This is what's happening in issue #170
Causing a fix in pytest-check 2.5.2
"""

import pytest
from pytest_check import check

@pytest.fixture(scope="session")
def fail_in_teardown():
    yield
    check.fail("Failed in teardown")

def test_fail_in_teardown(fail_in_teardown):
    assert 1 == 1  

@pytest.mark.skip
def test_skip():
    assert 1 == 1  
