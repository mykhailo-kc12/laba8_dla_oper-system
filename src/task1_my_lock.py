"""Task 1: одноразове блокування потоку через pipe."""

import os
import threading
import time


class MyLock:
    """Одноразовий блокувальник на основі програмного каналу pipe.

    Ідея:
    - pipe має кінець для читання і кінець для запису;
    - os.read() блокує потік, якщо в pipe ще немає даних;
    - os.write() записує 1 байт і розблоковує потік;
    - release() можна успішно викликати тільки один раз.
    """

    def __init__(self):
        self._read_fd, self._write_fd = os.pipe()
        self._state_lock = threading.Lock()
        self._released = False
        self._closed = False

    def wait(self):
        """Заблокувати потік до моменту виклику release()."""
        with self._state_lock:
            if self._closed:
                raise RuntimeError("MyLock is already closed")
            read_fd = self._read_fd

        data = os.read(read_fd, 1)
        return bool(data)

    def release(self):
        """Розблокувати один потік виконання.

        Повертає True, якщо розблокування виконано.
        Повертає False, якщо release() вже викликали раніше.
        """
        with self._state_lock:
            if self._closed:
                raise RuntimeError("MyLock is already closed")

            if self._released:
                return False

            os.write(self._write_fd, b"1")
            self._released = True
            return True

    def close(self):
        """Закрити файлові дескриптори pipe."""
        with self._state_lock:
            if self._closed:
                return

            for file_descriptor in (self._read_fd, self._write_fd):
                try:
                    os.close(file_descriptor)
                except OSError:
                    pass

            self._closed = True

    def __del__(self):
        """Гарантовано закрити pipe при видаленні об'єкта."""
        try:
            self.close()
        except Exception:
            pass


def worker(lock):
    """Функція, яку виконує додатковий потік."""
    print("Worker thread: started")
    print("Worker thread: waiting for release")

    lock.wait()

    print("Worker thread: unlocked and finished")


def run_demo(delay=1.0):
    """Демонстрація роботи MyLock з модулем threading."""
    lock = MyLock()
    thread = threading.Thread(target=worker, args=(lock,))

    print("Main thread: starting worker")
    thread.start()

    print("Main thread: worker is blocked now")
    time.sleep(delay)

    print("Main thread: releasing worker")
    lock.release()

    thread.join()
    lock.close()

    print("Main thread: demo finished")


if __name__ == "__main__":
    run_demo()
