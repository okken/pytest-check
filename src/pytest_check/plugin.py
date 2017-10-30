# -*- coding: utf-8 -*-

import pytest
import traceback
import sys
import inspect
import os

@pytest.fixture()
def check(request):
    return Check(request.node)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    evalxfail = getattr(item, '_evalxfail', None)
    failures = getattr(item, 'failures', None)
    if call.when == "call" and failures:
        if evalxfail and evalxfail.wasvalid() and evalxfail.istrue():
            report.outcome = "skipped"
            report.wasxfail = evalxfail.getexplanation()
        else:
            summary = 'Failed Checks: {}'.format(len(failures))
            if report.longrepr:
                report.sections.append((summary, "\n".join(failures)))
            else:
                longrepr = ['\n'.join(failures)]
                longrepr.append("-" * 60)
                longrepr.append(summary)
                report.longrepr = '\n'.join(longrepr)
            report.outcome = "failed"


class Check:

    def __init__(self, node):
        self.node = node
        self.node.failures = []

    def equal(self, a, b, msg=None):
        try:
            assert a == b
        except AssertionError:
            self.log_failure(msg)

    def not_equal(self, a, b):
        try:
            assert a != b
        except AssertionError:
            self.log_failure(msg)

    def is_true(self, x):
        try:
            assert bool(x) is True
        except AssertionError:
            self.log_failure(msg)

    def is_false(self, x):
        try:
            assert bool(x) is False
        except AssertionError:
            self.log_failure(msg)

    def is_not(self, a, b):
        try:
            assert a is not b
        except AssertionError:
            self.log_failure(msg)

    def is_none(self, x):
        try:
            assert x is None
        except AssertionError:
            self.log_failure(msg)

    def is_not_none(self, x):
        try:
            assert x is not None
        except AssertionError:
            self.log_failure(msg)

    def is_in(self, a, b):
        try:
            assert a in b
        except AssertionError:
            self.log_failure(msg)

    def not_in(self, a, b):
        try:
            assert a not in b
        except AssertionError:
            self.log_failure(msg)

    def is_instance(self, a, b):
        try:
            assert isinstance(a, b)
        except AssertionError:
            self.log_failure(msg)

    def not_is_instance(self, a, b):
        try:
            assert not isinstance(a, b)
        except AssertionError:
            self.log_failure(msg)

    def almost_equal(self, a, b, rel=None, abs=None, msg=None):
        """
        for rel and abs tolerance, see:
        See https://docs.pytest.org/en/latest/builtin.html#pytest.approx
        """
        try:
            assert a == approx(b, rel, abs)
        except AssertionError:
            self.log_failure(msg)

    def not_almost_equal(self, a, b, rel=None, abs=None, msg=None):
        """
        for rel and abs tolerance, see:
        See https://docs.pytest.org/en/latest/builtin.html#pytest.approx
        """
        try:
            assert a != approx(b, rel, abs)
        except AssertionError:
            self.log_failure(msg)

    def greater(self, a, b, msg=None):
        try:
            assert a > b
        except AssertionError:
            self.log_failure(msg)

    def greater_equal(self, a, b, msg=None):
        try:
            assert a >= b
        except AssertionError:
            self.log_failure(msg)

    def less(self, a, b, msg=None):
        try:
            assert a < b
        except AssertionError:
            self.log_failure(msg)

    def less_equal(self, a, b, msg=None):
        try:
            assert a <= b
        except AssertionError:
            self.log_failure(msg)

    def get_full_context(self, level):
        (frame, filename, line, funcname, contextlist) = inspect.stack()[level][0:5]
        filename = os.path.relpath(filename)
        context = contextlist[0].strip()
        return (filename, line, funcname, context)

    def log_failure(self, msg):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # last entry has the exception details
        exc_info = traceback.format_exception(exc_type, exc_value, exc_traceback)[-1]
        level = 3
        pseudo_trace = []
        funcname = ''
        while 'test_' not in funcname:
            (filename, line, funcname, context) = self.get_full_context(level)
            pseudo_trace.append('  {}, line {}, in {}() -> {}'.format(filename, line, funcname, context))
            level += 1
        pseudo_trace_str = '\n'.join(reversed(pseudo_trace))
        entry = 'FAILURE: {}\n{}\n{}'.format(msg if msg else "", pseudo_trace_str, exc_info)
        self.node.failures.append(entry)

