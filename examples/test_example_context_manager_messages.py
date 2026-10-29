from threading import Event, Thread

from pytest_check import check


def test_nested_messages():
    with check("outer message"):
        with check("inner message"):
            raise AssertionError("inner failure")
        raise AssertionError("outer failure")


def test_saved_messages():
    first = check("first message")
    second = check("second message")
    with first:
        raise AssertionError("first failure")
    with second:
        raise AssertionError("second failure")


def test_thread_messages():
    entered_first = Event()
    entered_second = Event()
    finished_first = Event()

    def first():
        with check("first message"):
            entered_first.set()
            assert entered_second.wait(5)
            raise AssertionError("first failure")
        finished_first.set()

    def second():
        assert entered_first.wait(5)
        with check("second message"):
            entered_second.set()
            assert finished_first.wait(5)
            raise AssertionError("second failure")

    threads = [Thread(target=first), Thread(target=second)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)
        assert not thread.is_alive()


def test_bound_helpers():
    with check("custom message") as context:
        assert context.equal(1, 1)
        assert not context.any_failures()
    with check:
        assert True
