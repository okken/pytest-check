def test_max_tb_line_thresholds_after_full_tracebacks(pytester):
    pytester.copy_example("examples/test_example_multiple_failures.py")
    result = pytester.runpytest("--check-max-tb=2", "--check-max-tb-line=5")
    result.assert_outcomes(failed=1)

    output = str(result.stdout)

    result.stdout.fnmatch_lines(
        [
            "*FAILURE: check 1 == 100",
            "*FAILURE: check 2 == 100",
            "*FAILURE: check 3 == 100, *",
            "*FAILURE: check 4 == 100, *",
            "*FAILURE: check 5 == 100, *",
            "*FAILURE: check 6 == 100",
        ],
    )
    assert output.count("test_multiple_failures() -> check.equal(i, 100)") == 5
    assert output.count("== 100, ") == 3


def test_max_tb_line_with_default_max_tb(pytester):
    pytester.copy_example("examples/test_example_multiple_failures.py")
    result = pytester.runpytest("--check-max-tb-line=4")
    result.assert_outcomes(failed=1)

    output = str(result.stdout)

    result.stdout.fnmatch_lines(
        [
            "*FAILURE: check 1 == 100",
            "*FAILURE: check 2 == 100, *",
            "*FAILURE: check 3 == 100, *",
            "*FAILURE: check 4 == 100, *",
            "*FAILURE: check 5 == 100",
        ],
    )
    assert output.count("test_multiple_failures() -> check.equal(i, 100)") == 4
    assert output.count("== 100, ") == 3


def test_max_tb_line_uses_inner_line_for_with_check(pytester):
    pytester.copy_example("examples/test_example_traceback.py")
    result = pytester.runpytest(
        "--check-max-tb=0",
        "--check-max-tb-line=1",
        "test_example_traceback.py::test_tb_ctx",
    )
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: assert message*",
            '*test_example_traceback.py:* in helper2_ctx() -> assert 1 == 2, "assert message"',
        ],
    )
    result.stdout.no_fnmatch_line('*-> with check("check message"):*')


def test_max_tb_line_includes_line_and_exception_summary(pytester):
    pytester.copy_example("examples/test_example_multi_check_raises.py")
    result = pytester.runpytest("--check-max-tb=1", "--check-max-tb-line=4")
    result.assert_outcomes(failed=1)
    output = str(result.stdout)
    assert (
        "FAILURE: list index out of range, "
        "test_example_multi_check_raises.py:6 in test_multi_check_raises() "
        '-> assert lst_1[-1] == "Fail 2": IndexError: list index out of range'
    ) in output
