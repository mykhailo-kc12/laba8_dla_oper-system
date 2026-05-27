"""Tests for task1_my_lock.py."""

import threading

from src.task1_my_lock import MyLock


def test_my_lock_blocks_until_release():
    """Перевіряє, що потік блокується і продовжує роботу після release."""
    lock = MyLock()

    started = threading.Event()
    unblocked = threading.Event()

    def worker():
        started.set()
        lock.wait()
        unblocked.set()

    thread = threading.Thread(target=worker)
    thread.start()

    assert started.wait(timeout=1)
    assert not unblocked.wait(timeout=0.05)

    assert lock.release() is True
    assert unblocked.wait(timeout=1)

    thread.join(timeout=1)

    assert not thread.is_alive()
    assert lock.release() is False

    lock.close()
