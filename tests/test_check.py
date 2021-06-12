# -*- coding: utf-8 -*-

# properly formatted tests in
# multiline strings contain blank lines with spaces, freaks out flake8

# flake8: noqa

import pytest_check as check


def test_equal():
    check.equal(1, 1)


def test_not_equal():
    check.not_equal(1, 2)


def test_is():
    x = ["foo"]
    y = x
    check.is_(x, y)


def test_is_not():
    x = ["foo"]
    y = ["foo"]
    check.is_not(x, y)


def test_is_true():
    check.is_true(True)


def test_is_false():
    check.is_false(False)


def test_is_none():
    a = None
    check.is_none(a)


def test_is_not_none():
    a = 1
    check.is_not_none(a)


def test_is_in():
    check.is_in(2, [1, 2, 3])


def test_is_not_in():
    check.is_not_in(4, [1, 2, 3])


def test_is_instance():
    check.is_instance(1, int)


def test_is_not_instance():
    check.is_not_instance(1, str)


def test_almost_equal():
    check.almost_equal(1, 1)
    check.almost_equal(1, 1.1, abs=0.2)
    check.almost_equal(2, 1, rel=1)


def test_not_almost_equal():
    check.not_almost_equal(1, 2)
    check.not_almost_equal(1, 2.1, abs=0.1)
    check.not_almost_equal(3, 1, rel=1)


def test_greater():
    check.greater(2, 1)


def test_greater_equal():
    check.greater_equal(2, 1)
    check.greater_equal(1, 1)


def test_less():
    check.less(1, 2)


def test_less_equal():
    check.less_equal(1, 2)
    check.less_equal(1, 1)


def test_watch_them_all_fail(testdir):
    testdir.makepyfile(
        """
        import pytest_check as check

        def test_equal():
            check.equal(1,2)

        def test_not_equal():
            check.not_equal(1,1)

        def test_is():
            x = ["foo"]
            y = ["foo"]
            check.is_(x, y)

        def test_is_not():
            x = ["foo"]
            y = x
            check.is_not(x, y)

        def test_is_true():
            check.is_true(False)


        def test_is_false():
            check.is_false(True)


        def test_is_none():
            a = 1
            check.is_none(a)


        def test_is_not_none():
            a = None
            check.is_not_none(a)


        def test_is_in():
            check.is_in(4, [1, 2, 3])


        def test_is_not_in():
            check.is_not_in(2, [1, 2, 3])


        def test_is_instance():
            check.is_instance(1, str)


        def test_is_not_instance():
            check.is_not_instance(1, int)

        def test_almost_equal():
            check.almost_equal(1, 2)
            check.almost_equal(1, 2.1, abs=0.1)
            check.almost_equal(1, 3, rel=1)


        def test_not_almost_equal():
            check.not_almost_equal(1, 1)
            check.not_almost_equal(1, 1.1, abs=0.1)
            check.not_almost_equal(1, 2, rel=1)


        def test_greater():
            check.greater(1, 2)
            check.greater(1, 1)


        def test_greater_equal():
            check.greater_equal(1, 2)


        def test_less():
            check.less(2, 1)
            check.less(1, 1)


        def test_less_equal():
            check.less_equal(2, 1)
            #check.equal(2, 1)

    """
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=18, passed=0)


def test_check_xfail(testdir):
    testdir.makepyfile(
        """
        import pytest_check as check
        import pytest

        @pytest.mark.xfail()
        def test_fail():
            check.equal(1, 2)
    """
    )

    result = testdir.runpytest()
    result.assert_outcomes(xfailed=1)
    result.stdout.fnmatch_lines(["* 1 xfailed *"])


def test_check_xfail_strict(testdir):
    testdir.makepyfile(
        """
        import pytest_check as check
        import pytest

        @pytest.mark.xfail(strict=True)
        def test_fail():
            check.equal(1, 2)
    """
    )

    result = testdir.runpytest()
    result.assert_outcomes(xfailed=1)
    result.stdout.fnmatch_lines(["* 1 xfailed *"])


def test_check_xpassed(testdir):
    testdir.makepyfile(
        """
        import pytest_check as check
        import pytest

        @pytest.mark.xfail()
        def test_fail():
            check.equal(1, 1)
    """
    )

    result = testdir.runpytest()

    result.assert_outcomes(xpassed=1)

    result.stdout.fnmatch_lines(["* 1 xpassed *"])


def test_check_xpassed_strict(testdir):
    testdir.makepyfile(
        """
        import pytest_check as check
        import pytest

        @pytest.mark.xfail(strict=True)
        def test_pass():
            check.equal(1, 1)
    """
    )

    result = testdir.runpytest()

    result.assert_outcomes(failed=1)

    result.stdout.fnmatch_lines(["* 1 failed *"])


def test_check_and_assert(testdir):
    testdir.makepyfile(
        """
        import pytest_check as check
        import pytest

        def test_fail_check():
            check.equal(1, 2)

        def test_fail_assert():
            assert 1 == 2
    """
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=2)
    result.stdout.fnmatch_lines(["* 2 failed *"])


def test_stop_on_fail(testdir):
    testdir.makepyfile(
        """
        import pytest_check as check

        class TestStopOnFail():

            def test_1(self):
                check.equal(1, 1)
                check.equal(1, 2)
                check.equal(1, 3)


            def test_2(self):
                check.equal(1, 1)
                check.equal(1, 2)
                check.equal(1, 3)
    """
    )

    result = testdir.runpytest("-x")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*> * check.equal(1, 2)*"])
