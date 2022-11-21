from pytest import LineMatcher


def test_traceback_style_no(pytester):
    pytester.copy_example("examples/test_example_tb_style.py")
    result = pytester.runpytest("--junitxml=output.xml", "--tb=no")
    result.assert_outcomes(failed=1, passed=0)
    with open("output.xml") as f:
        lines = LineMatcher(f.readlines())
        lines.no_fnmatch_line("*run_helper1()*")


def test_traceback_style_default(pytester):
    pytester.copy_example("examples/test_example_tb_style.py")
    result = pytester.runpytest("--junitxml=output.xml")
    result.assert_outcomes(failed=1, passed=0)
    with open("output.xml") as f:
        lines = LineMatcher(f.readlines())
        lines.fnmatch_lines("*run_helper1()*")
