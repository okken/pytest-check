def test_setup_failure(testdir):
    testdir.makepyfile(
        """
        import pytest
        import pytest_check as check

        @pytest.fixture()
        def a_fixture():
            check.equal(1, 2)

        def test_1(a_fixture):
            pass
        """
    )
    result = testdir.runpytest()
    result.assert_outcomes(errors=1)
    result.stdout.fnmatch_lines(["* check.equal(1, 2)*"])


def test_teardown_failure(testdir):
    testdir.makepyfile(
         """
         import pytest
         import pytest_check as check

         @pytest.fixture()
         def a_fixture():
             yield
             check.equal(1, 2)

         def test_1(a_fixture):
             pass
         """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1, errors=1)
    result.stdout.fnmatch_lines(["* check.equal(1, 2)*"])
