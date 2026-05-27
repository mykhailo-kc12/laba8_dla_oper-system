"""Tests for task2_file_reader.py."""

import pytest

from src.task2_file_reader import FileReaderThread
from src.task2_file_reader import read_file_with_thread


def test_file_reader_thread_reads_file_content(tmp_path):
    """Перевіряє, що потік правильно читає текстовий файл."""
    file_path = tmp_path / "input.txt"
    file_path.write_text("Hello from thread!\n", encoding="utf-8")

    reader = FileReaderThread(file_path)
    reader.start()
    reader.join(timeout=1)

    assert not reader.is_alive()
    assert reader.get_content() == "Hello from thread!\n"


def test_read_file_with_thread_returns_content(tmp_path):
    """Перевіряє допоміжну функцію читання файлу через потік."""
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Line 1\nLine 2\n", encoding="utf-8")

    content = read_file_with_thread(file_path)

    assert content == "Line 1\nLine 2\n"


def test_file_reader_thread_raises_error_for_missing_file(tmp_path):
    """Перевіряє обробку ситуації, коли файл не існує."""
    file_path = tmp_path / "missing.txt"

    reader = FileReaderThread(file_path)
    reader.start()
    reader.join(timeout=1)

    with pytest.raises(FileNotFoundError):
        reader.get_content()
