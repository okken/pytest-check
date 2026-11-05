import importlib.metadata
import sys

import pytest
from packaging import version


def _has_pytest_plugin(name: str) -> bool:
    """Whether a pytest11 entry point called ``name`` is installed.

    The tests that use these markers run the plugin in a ``pytester`` run, so
    being importable is not enough: pytest only loads plugins it finds through
    their entry points.
    """
    if sys.version_info >= (3, 10):
        plugins = importlib.metadata.entry_points(group="pytest11")
    else:
        plugins = importlib.metadata.entry_points().get("pytest11", [])
    return any(ep.name == name for ep in plugins)


require_pytest_7_3 = pytest.mark.skipif(
    version.parse(pytest.__version__) < version.parse("7.3.0"),
    reason="summary message only supported on pytest7.3+",
)

require_pytest_reportlog = pytest.mark.skipif(
    not _has_pytest_plugin("pytest_reportlog"),
    reason="requires pytest-reportlog",
)

require_pytest_run_parallel = pytest.mark.skipif(
    not _has_pytest_plugin("run-parallel"),
    reason="requires pytest-run-parallel",
)

require_pytest_swarm = pytest.mark.skipif(
    not _has_pytest_plugin("pytest-swarm"),
    reason="requires pytest-swarm",
)

require_pytest_freethreaded = pytest.mark.skipif(
    not _has_pytest_plugin("freethreaded"),
    reason="requires pytest-freethreaded",
)
