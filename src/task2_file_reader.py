"""Task 2: читання файлу в окремому потоці."""

from pathlib import Path
import threading
import time


class FileReaderThread(threading.Thread):
    """Потік-нащадок Thread для виконання I/O-bound завдання.

    Клас читає файл у методі run().
    Основний потік може запустити цей об'єкт, дочекатися завершення
    через join() і забрати результат через get_content().
    """

    def __init__(self, file_path, encoding="utf-8"):
        super().__init__()
        self.file_path = Path(file_path)
        self.encoding = encoding
        self.content = ""
        self.error = None

    def run(self):
        """Основна робота потоку: читання файлу."""
        try:
            # Невелика пауза показує, що операція виконується окремо.
            time.sleep(0.05)
            self.content = self.file_path.read_text(encoding=self.encoding)
        except OSError as error:
            self.error = error

    def get_content(self):
        """Повернути прочитаний текст або підняти помилку читання."""
        if self.error is not None:
            raise self.error

        return self.content


def read_file_with_thread(file_path):
    """Запустити читання файлу в потоці та повернути його контент."""
    reader = FileReaderThread(file_path)

    print("Main thread: starting file reader")
    reader.start()

    while reader.is_alive():
        print("Main thread: waiting for file reading")
        reader.join(timeout=0.1)

    content = reader.get_content()

    print("Main thread: file reading finished")
    return content


def run_demo(file_path):
    """Демонстрація роботи читання файлу через Thread."""
    content = read_file_with_thread(file_path)

    print("File content:")
    print(content)


if __name__ == "__main__":
    run_demo("data/sample.txt")
