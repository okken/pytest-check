def test_log(testdir):
    testdir.makepyfile("""
    import logging
    from pytest_check import check

    log = logging.getLogger(__name__)

    records = None

    # will fail and produce logs
    def test_logging(caplog):
        global records
        check.call_on_fail(log.error)
        log.error('one')
        check.equal(1, 2, "two")
        log.error('three')
        check.equal(1, 2, "four")
        log.error('five')
        records = caplog.records

    # consumes logs from previous test
    # should pass
    def test_log_content():
        assert 'one' in records[0].message
        assert 'two' in records[1].message
        assert 'three' in records[2].message
        assert 'four' in records[3].message
        assert 'five' in records[4].message
    """)

    result = testdir.runpytest()
    result.assert_outcomes(failed=1, passed=1)


def test_print(testdir):
    testdir.makepyfile(
        """
        from pytest_check import check

        def test_with_print():
            check.call_on_fail(print)
            print('one')
            check.equal(1, 2, "two")
            print('three')
            check.equal(1, 2, "four")
            print('five')
        """)
    result = testdir.runpytest()
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*one*", "*two*", "*three*", "*four*", "*five*"])


def test_session_callback_persists_across_tests(testdir):
    testdir.makeconftest(
        """
        import pytest
        from pytest_check import check

        @pytest.fixture(scope="session", autouse=True)
        def register_callback():
            check.call_on_fail(print)
        """
    )
    testdir.makepyfile(
        """
        from pytest_check import check

        def test_one():
            check.equal(1, 2)

        def test_two():
            check.equal(3, 4)
        """
    )

    result = testdir.runpytest()
    result.assert_outcomes(failed=2)
    result.stdout.fnmatch_lines(["*check 1 == 2*", "*check 3 == 4*"])
