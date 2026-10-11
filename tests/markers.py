import importlib.util

import pytest
from packaging import version


require_pytest_7_3 = pytest.mark.skipif(
    version.parse(pytest.__version__) < version.parse("7.3.0"),
    reason="summary message only supported on pytest7.3+",
)

require_pytest_reportlog = pytest.mark.skipif(
    importlib.util.find_spec("pytest_reportlog") is None,
    reason="requires pytest-reportlog",
)

require_pytest_run_parallel = pytest.mark.skipif(
    importlib.util.find_spec("pytest_run_parallel") is None,
    reason="requires pytest-run-parallel",
)

require_pytest_swarm = pytest.mark.skipif(
    importlib.util.find_spec("pytest_swarm") is None,
    reason="requires pytest-swarm",
)

require_pytest_freethreaded = pytest.mark.skipif(
    importlib.util.find_spec("pytest_freethreaded") is None,
    reason="requires pytest-freethreaded",
)
