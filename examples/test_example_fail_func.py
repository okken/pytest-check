from pytest_check import check


def test_one_failure():
    check.fail('one')


def test_two_failures():
    check.fail('one')
    check.fail('two')
