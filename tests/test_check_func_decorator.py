from pytest_check import check_func

# properly formatted tests in
# multiline strings contain blank lines with spaces, freaks out flake8

# flake8: noqa

@check_func
def is_five(a):
    assert a == 5


def test_pass():
    is_five(5)


def test_fail(testdir):
    testdir.makepyfile(
        """
        from pytest_check import check_func
        
        @check_func
        def is_four(a):
            assert a == 4

        def test_all_four():
            is_four(1)
            is_four(2)
            is_four(3)
            is_four(4)
    """
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines([
        "*FAILURE: assert 1 == 4*",
        "*FAILURE: assert 2 == 4*",
        "*FAILURE: assert 3 == 4*",
        "*Failed Checks: 3*",
    ])
