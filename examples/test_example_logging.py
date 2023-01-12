import logging
from pytest_check import check

log = logging.getLogger(__name__)


def test_with_logging():
    """
    Try this with:
    > pytest --log-format="%(levelname)s - %(message)s" --check-max-tb=4
    or:
    > pytest --log-cli-level=DEBUG \
       --log-format="%(levelname)s - %(message)s" --check-max-tb=4 \
       --show-capture=no --no-summary
    """
    def log_failure(message):
        log.error(message)
    check.call_on_fail(log_failure)
    log.debug('debug message')
    check.equal(1, 2, "after debug")
    log.info('info message')
    check.equal(1, 2, "after info")
    log.warning('warning message')
    check.equal(1, 2, "after warning")
    log.error('error message')
    check.equal(1, 2, "after error")


def test_with_print():
    """
    Try this with:
    > pytest examples/test_example_logging.py::test_with_print --check-max-tb=2
    or:
    > pytest examples/test_example_logging.py::test_with_print -s \
      --check-max-tb=2  --no-summary
    """
    check.call_on_fail(print)
    print('first message')
    check.equal(1, 2, "after first")
    print('second message')
    check.equal(1, 2, "after second")
    print('last message')
