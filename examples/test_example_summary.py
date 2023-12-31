from pytest_check import check

def test_assert_no_msg():
    a, b = 1, 2
    assert a == b


def test_assert_msg():
    a, b = 1, 2
    assert a == b, f"comment about a={a} != b={b}"


def test_check_no_msg():
    a, b = 1, 2
    check.equal(a, b)


def test_check_msg():
    a, b = 1, 2
    check.equal(a, b, f"comment about a={a} != b={b}")
