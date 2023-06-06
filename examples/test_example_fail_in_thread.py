from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread


import pytest_check as check


def force_fail(comparison):
    check.equal(1 + 1, comparison, f"1 + 1 is 2, not {comparison}")


def test_threadpool():
    with ThreadPoolExecutor() as executor:
        task = executor.submit(force_fail, 3)
        task.result()


def test_threading():
    t = Thread(target=force_fail, args=(4, ))
    t.start()
    t.join()
