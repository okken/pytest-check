import pytest

from pytest_check import check_log, pseudo_traceback


@pytest.fixture(autouse=True)
def reset_check_log_state():
    check_log.clear_failures()
    check_log.should_use_color = False
    yield
    check_log.should_use_color = False
    check_log.clear_failures()


def test_is_user_trace_frame_filters_internal_and_module_frames():
    assert not pseudo_traceback._is_user_trace_frame("site-packages/pkg/mod.py", "fn")
    assert not pseudo_traceback._is_user_trace_frame("src/pytest_check/plugin.py", "fn")
    assert not pseudo_traceback._is_user_trace_frame("project/test_file.py", "<module>")
    assert pseudo_traceback._is_user_trace_frame("project/test_file.py", "test_func")


def test_extract_exception_summary_handles_empty_and_type_only_lines():
    summary = pseudo_traceback._extract_exception_summary(
        [
            "Traceback (most recent call last)",
            'File "example.py", line 1, in test_func\n    1/0',
            "",
            "ValueError",
        ]
    )
    assert summary == "ValueError"


def test_extract_exception_summary_skips_blank_lines():
    summary = pseudo_traceback._extract_exception_summary(
        [
            "Traceback (most recent call last)",
            "",
        ]
    )
    assert summary == ""


def test_build_single_line_trace_respects_tb_style_no(monkeypatch):
    monkeypatch.setattr(pseudo_traceback, "_traceback_style", "no")
    assert pseudo_traceback._build_single_line_trace_str(None, color=False) == ""


def test_build_single_line_trace_uses_tb_frame_and_color(monkeypatch):
    monkeypatch.setattr(pseudo_traceback, "_traceback_style", "auto")
    tb = [
        'File "/tmp/test_file.py", line 9, in helper\n    do_it()\n',
        "ValueError",
    ]

    line = pseudo_traceback._build_single_line_trace_str(tb, color=True)

    assert line.startswith(pseudo_traceback.COLOR_RED)
    assert "in helper() -> do_it(): ValueError" in line


def test_build_single_line_trace_fallback_breaks_for_non_user_stack_frame(monkeypatch):
    monkeypatch.setattr(pseudo_traceback, "_traceback_style", "auto")
    tb = ['File "/x/site-packages/pkg/mod.py", line 3, in helper\n    boom()\n']

    monkeypatch.setattr(pseudo_traceback.inspect, "stack", lambda: [None, None, None, object()])
    monkeypatch.setattr(
        pseudo_traceback,
        "get_full_context",
        lambda _frame: ("site-packages/pkg/mod.py", 3, "helper", "boom()", {}, False),
    )

    assert pseudo_traceback._build_single_line_trace_str(tb, color=False) == ""


def test_build_single_line_trace_fallback_skips_hidden_then_returns_colored(monkeypatch):
    monkeypatch.setattr(pseudo_traceback, "_traceback_style", "auto")

    frames = [None, None, None, object(), object()]
    contexts = [
        ("tests/test_file.py", 12, "helper_hidden", "first()", {"x": 1}, True),
        ("tests/test_file.py", 13, "worker", "second()", {"x": 2}, False),
    ]

    monkeypatch.setattr(pseudo_traceback.inspect, "stack", lambda: frames)
    monkeypatch.setattr(pseudo_traceback, "get_full_context", lambda _frame: contexts.pop(0))

    line = pseudo_traceback._build_single_line_trace_str(None, color=True)

    assert line.startswith(pseudo_traceback.COLOR_RED)
    assert "in worker() -> second()" in line


def test_build_single_line_trace_hidden_test_frame_falls_through_to_empty(monkeypatch):
    monkeypatch.setattr(pseudo_traceback, "_traceback_style", "auto")
    monkeypatch.setattr(pseudo_traceback.inspect, "stack", lambda: [None, None, None, object()])
    monkeypatch.setattr(
        pseudo_traceback,
        "get_full_context",
        lambda _frame: ("tests/test_file.py", 12, "test_hidden", "ignored()", {}, True),
    )

    assert pseudo_traceback._build_single_line_trace_str(None, color=False) == ""


def test_log_failure_handles_empty_single_line_trace_path(monkeypatch):
    monkeypatch.setattr(check_log, "_build_pseudo_trace_str", lambda *_args, **_kwargs: "pseudo")
    monkeypatch.setattr(
        check_log, "_build_single_line_trace_str", lambda *_args, **_kwargs: ""
    )

    check_log._max_tb = 1
    check_log._max_tb_line = 2

    check_log.log_failure("first")
    check_log.log_failure("second")

    failures = check_log.get_failures()
    assert len(failures) == 2
    assert failures[1] == "FAILURE: second"
    check_log.clear_failures()