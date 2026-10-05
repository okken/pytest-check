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
        """
    )
    result = testdir.runpytest()
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*one*", "*two*", "*three*", "*four*", "*five*"])


def test_logging_to_a_file_example(pytester):
    """
    Verify the examples/logging_to_a_file example (documented in the README
    "Logging to a file" section) correctly logs check failures to session.log.
    """
    pytester.copy_example("examples/logging_to_a_file/conftest.py")
    pytester.copy_example("examples/logging_to_a_file/test_file_logging.py")

    result = pytester.runpytest()
    result.assert_outcomes(failed=2)

    log_file = pytester.path / "session.log"
    assert log_file.is_file()

    content = log_file.read_text()
    assert "Starting test run" in content
    assert "FAILURE: check 1 == 2" in content
    assert "FAILURE: check 5 == 6" in content
