from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread


from pytest_check import check


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
