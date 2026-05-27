"""Tests for task3_calculations.py."""

import pytest

from src.task3_calculations import calculate_catalan_numbers
from src.task3_calculations import calculate_prime_numbers
from src.task3_calculations import is_prime
from src.task3_calculations import run_calculations


def test_calculate_catalan_numbers():
    """Перевіряє правильність перших чисел Каталана."""
    expected = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862]

    assert calculate_catalan_numbers(10) == expected


def test_calculate_catalan_numbers_zero_count():
    """Перевіряє випадок, коли треба обчислити 0 чисел."""
    assert calculate_catalan_numbers(0) == []


def test_calculate_catalan_numbers_negative_count():
    """Перевіряє помилку для від'ємної кількості."""
    with pytest.raises(ValueError):
        calculate_catalan_numbers(-1)


def test_is_prime():
    """Перевіряє функцію визначення простого числа."""
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False
    assert is_prime(17) is True
    assert is_prime(21) is False


def test_calculate_prime_numbers():
    """Перевіряє правильність перших простих чисел."""
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    assert calculate_prime_numbers(10) == expected


def test_calculate_prime_numbers_zero_count():
    """Перевіряє випадок, коли треба обчислити 0 простих чисел."""
    assert calculate_prime_numbers(0) == []


def test_calculate_prime_numbers_negative_count():
    """Перевіряє помилку для від'ємної кількості."""
    with pytest.raises(ValueError):
        calculate_prime_numbers(-1)


def test_run_calculations():
    """Перевіряє одночасний запуск двох обчислювальних потоків."""
    catalan_numbers, prime_numbers = run_calculations(5, 6)

    assert catalan_numbers == [1, 1, 2, 5, 14]
    assert prime_numbers == [2, 3, 5, 7, 11, 13]
