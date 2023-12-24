from pytest_check import check


def test_baseline():
    a, b = 1, 2
    check.equal(a, b)


def test_message():
    a, b = 1, 2
    check.equal(a, b, f"comment about a={a} != b={b}")
