from typing import Callable, Dict, List, Optional

import pytest


@pytest.mark.parametrize(
    "maxfail,expected_outcomes,expected_lines",
    [
        (
            1,
            {"failed": 1, "passed": 0},
            ["*AssertionError: one*"],
        ),
        (
            2,
            {"failed": 2, "passed": 0},
            [
                "*FAILURE: one",
                "*FAILURE: two",
                "*FAILURE: three",
                "*Failed Checks: 3*",
            ],
        ),
        (
            3,
            {"failed": 2, "passed": 1},
            None,
        ),
    ],
)
def test_maxfail_behavior(
    run_example_test: Callable,
    maxfail: int,
    expected_outcomes: Dict[str, int],
    expected_lines: Optional[List[str]],
) -> None:
    """
    Test that --maxfail correctly stops after N failed tests (not checks).

    - maxfail=1: Should stop after first failed check
    - maxfail=2: Should stop after 2 tests (not checks)
    - maxfail=3: Should not stop on checks, runs at least 3 tests
    """
    result = run_example_test("test_example_maxfail.py", None, f"--maxfail={maxfail}")
    result.assert_outcomes(**expected_outcomes)
    if expected_lines:
        result.stdout.fnmatch_lines(expected_lines)
