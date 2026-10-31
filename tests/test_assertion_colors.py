import re

import pytest


@pytest.mark.parametrize("color", ["yes", "no"])
@pytest.mark.parametrize("workers", [0, 2])
def test_mixed_check_and_assert_keep_source_highlighting(pytester, color, workers):
    if color == "yes":
        pytest.importorskip("pygments")
    if workers:
        pytest.importorskip("xdist")
    pytester.makepyfile(
        """
        from pytest_check import check

        def test_mixed():
            value = 1
            check.equal(value, 2)
            assert value == 3
        """
    )
    arguments = [f"--color={color}", "--code-highlight=yes"]
    if workers:
        arguments.extend(["-n", str(workers)])
    result = pytester.runpytest(*arguments)
    result.assert_outcomes(failed=1)
    output = result.stdout.str()
    assert "Failed Checks: 1" in output
    assert "check 1 == 2" in output
    if color == "yes":
        assert re.search(r"\x1b\[[0-9;]*massert\x1b\[[0-9;]*m", output)
    else:
        assert "assert value == 3" in output
        assert "\x1b[" not in output
