"""
An example to show hwo tracebacks work with hlper functions.
We've got.
1. test -> helper -> helper -> check function
2. test -> helper -> helper -> check context manager -> assert
3. test -> check context manager -> helper -> helper -> assert

The 3rd option has the worst tb right now, as it doesn't show the helper functions.

Takeaway: Keep the context manager close to the assert.

Possible todo item: Maybe the pseudo-tb could inspect the incoming exception more.

"""

from pytest_check import check


# check.equal in helper


def helper_func():
    helper2_func()


def helper2_func():
    check.equal(1, 2, "custom")


def test_tb_func(check):
    helper_func()


# ctx in helper


def helper_ctx():
    helper2_ctx()


def helper2_ctx():
    with check("check message"):
        assert 1 == 2, "assert message"


def test_tb_ctx(check):
    helper_ctx()


# ctx in test func, assert in helper


def helper_assert():
    helper2_assert()


def helper2_assert():
    assert 1 == 2, "assert message"


def test_tb_ctx_assert(check):
    with check("check message"):
        helper_assert()
