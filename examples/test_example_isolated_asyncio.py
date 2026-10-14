"""
This was something that failed correctly pre 3.0.0
Specifically, it was failing correctly in version 2.9.1
And passed incorrectly in 3.0.0 and 3.0.1

Issue #210: 
  pytest-check 3.0: failed checks in IsolatedAsyncioTestCase tests 
  are not reported
"""

import unittest

from pytest_check import check


class TestAsync(unittest.IsolatedAsyncioTestCase):
    async def test_failed_check(self):
        with check:
            self.fail("async check failed")