"""
This example is used in the README.md
To run this example, first `pip install httpx`

This example is NOT tested by the test suite.
"""
import httpx
from pytest_check import check


def test_httpx_get():
    r = httpx.get("https://www.example.org/")
    # bail if bad status code
    assert r.status_code == 200
    # but if we get here
    # no need to stop on any failure
    with check:
        assert r.is_redirect is False
    with check:
        assert r.encoding == "utf-8"
    with check:
        assert "Example Domain" in r.text


def test_httpx_get_with_helpers():
    r = httpx.get("https://www.example.org/")
    assert r.status_code == 200
    check.is_false(r.is_redirect)
    check.equal(r.encoding, "utf-8")
    check.is_in("Example Domain", r.text)
