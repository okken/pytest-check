"""
"with check.check:" - bad
"with check:" - good

However, we want both to work.
"""


def test_check(check):
    with check:
        assert True


def test_check_check(check):
    "Deprecated, but should still work for now"
    with check.check:
        assert True
