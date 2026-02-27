import logging
import pytest
from pytest_check import check

@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    # logging config
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler('session.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('--- %(asctime)s.%(msecs)03d ---\n%(message)s', 
                                      datefmt='%Y-%m-%d %H:%M:%S'))
    log.addHandler(fh)
    # log start of tests
    log.info("---------\nStarting test run\n---------")
    # have check failures log to file
    def log_failure(message):
        log.error(message)
    check.call_on_fail(log_failure)


