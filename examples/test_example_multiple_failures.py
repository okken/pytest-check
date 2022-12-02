from pytest_check import check


def test_multiple_failures():
    for i in range(1, 11):
        check.equal(i, 100)
