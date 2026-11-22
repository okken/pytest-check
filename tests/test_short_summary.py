import re

import pytest

from tests.markers import require_pytest_7_3


@require_pytest_7_3
@pytest.mark.parametrize("color", ["no", "yes"])
def test_summary_keeps_literal_failure_marker(pytester, color):
    pytester.makepyfile(
        test_report="""
        from pytest_check import check

        def test_check():
            check.equal(1, 2, "saw FAILURE: input")
            check.equal(3, 4, "second failure")
        """
    )
    result = pytester.runpytest("-q", f"--color={color}")
    result.assert_outcomes(failed=1)

    output = re.sub(r"\x1b\[[0-9;]*m", "", result.stdout.str())
    assert [line for line in output.splitlines() if line.startswith("FAILED ")] == [
        "FAILED test_report.py::test_check - check 1 == 2: saw FAILURE: input"
    ]
