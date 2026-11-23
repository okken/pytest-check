from textwrap import indent

import pytest
from _pytest.pytester import Pytester

from pytest_check import any_failures, check


STYLES = ["plain", "configured", "raises", "callable"]


def _body(style: str, statement: str) -> str:
    if style == "callable":
        return f"check.raises(ValueError, lambda: {statement})"
    contexts = {
        "plain": "check",
        "configured": "configured",
        "raises": "check.raises(ValueError)",
    }
    return f"with {contexts[style]}:\n    {statement}"


@pytest.mark.parametrize("style", STYLES)
@pytest.mark.parametrize("event, outcome", [("skip", "skipped"), ("xfail", "xfailed")])
@pytest.mark.parametrize("stop_on_fail", [False, True])
def test_pytest_outcomes_propagate(
    pytester: Pytester, style: str, event: str, outcome: str, stop_on_fail: bool
) -> None:
    body = _body(style, f"pytest.{event}('control flow reason')")
    pytester.makepyfile(
        "import pytest\nfrom pytest_check import check\n\n"
        "configured = check('context message')\n\n"
        f"def test_outcome():\n{indent(body, '    ')}\n"
        "    pytest.fail('continued after control flow')\n"
    )
    result = pytester.runpytest("-q", *("-x",) if stop_on_fail else ())
    result.assert_outcomes(**{outcome: 1})
    result.stdout.no_fnmatch_line("*FAILURE:*")
    result.stdout.no_fnmatch_line("*continued after control flow*")


@pytest.mark.parametrize("style", STYLES)
@pytest.mark.parametrize(
    "exc_type", ["KeyboardInterrupt", "SystemExit", "GeneratorExit", "ControlFlow", "pytest.exit.Exception"]
)
def test_unmatched_control_exceptions_propagate(
    pytester: Pytester, style: str, exc_type: str
) -> None:
    body = _body(style, "raise_event()")
    pytester.makepyfile(
        "import pytest\nfrom pytest_check import any_failures, check\n\n"
        "class ControlFlow(BaseException):\n    pass\n\n"
        "def test_propagation():\n"
        f"    event = {exc_type}('stop')\n"
        "    configured = check('context message')\n"
        "    def raise_event():\n        raise event\n"
        "    with pytest.raises(type(event)) as caught:\n"
        f"{indent(body, '        ')}\n"
        "    assert caught.value is event\n"
        "    assert not any_failures()\n"
        + ("    assert configured.msg is None\n" if style == "configured" else "")
    )
    result = pytester.runpytest("-q")
    result.assert_outcomes(passed=1)


@pytest.mark.parametrize("style", ["raises", "callable"])
@pytest.mark.parametrize(
    "expected, event",
    [
        (SystemExit, SystemExit(2)),
        ((KeyboardInterrupt, SystemExit), SystemExit(2)),
        (BaseException, KeyboardInterrupt()),
        (pytest.skip.Exception, pytest.skip.Exception("explicit skip")),
        (BaseException, pytest.xfail.Exception("explicit xfail")),
        (pytest.exit.Exception, pytest.exit.Exception("explicit exit")),
    ],
)
def test_explicitly_expected_control_exceptions_are_still_checked(
    style: str, expected: type | tuple[type, ...], event: BaseException
) -> None:
    def raise_event() -> None:
        raise event

    if style == "callable":
        check.raises(expected, raise_event)
    else:
        with check.raises(expected) as caught:
            raise_event()
        assert caught.value is event
    assert not any_failures()


@pytest.mark.parametrize("style", STYLES)
@pytest.mark.parametrize("statement", ["pytest.fail('soft failure')", "raise TypeError('ordinary failure')"])
def test_normal_failures_remain_soft(pytester: Pytester, style: str, statement: str) -> None:
    if style == "callable" and statement.startswith("raise "):
        statement = "(_ for _ in ()).throw(TypeError('ordinary failure'))"
    body = _body(style, statement)
    pytester.makepyfile(
        "import pytest\nfrom pytest_check import check\n\n"
        "configured = check('context message')\n\n"
        f"def test_failures():\n{indent(body, '    ')}\n"
        "    check.equal(1, 2, 'second failure')\n"
        "    print('continued after normal failure')\n"
    )
    result = pytester.runpytest("-q", "-s")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*continued after normal failure*", "*Failed Checks: 2*"])


@pytest.mark.parametrize("style", STYLES)
def test_exit_stops_the_pytest_session(pytester: Pytester, style: str) -> None:
    body = _body(style, "pytest.exit('stop the session', returncode=4)")
    pytester.makepyfile(
        "import pytest\nfrom pytest_check import check\n\n"
        "configured = check('context message')\n\n"
        f"def test_stop():\n{indent(body, '    ')}\n"
        "    pytest.fail('continued after session exit')\n\n"
        "def test_after():\n    print('ran after session exit')\n"
    )
    result = pytester.runpytest_subprocess("-q", "-s")
    assert result.ret == 4
    result.stdout.no_fnmatch_line("*continued after session exit*")
    result.stdout.no_fnmatch_line("*ran after session exit*")
