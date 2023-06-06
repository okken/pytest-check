from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread


import pytest_check as check


def always_pass():
    check.equal(1 + 1, 2)


def test_threadpool():
    with ThreadPoolExecutor() as executor:
        task = executor.submit(always_pass)
        task.result()


def test_threading():
    t = Thread(target=always_pass)
    t.start()
    t.join()
