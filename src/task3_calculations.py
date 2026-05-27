"""Task 3: обчислення чисел Каталана і простих чисел у потоках."""

import argparse
import math
import threading


def non_negative_int(value):
    """Перевірити, що параметр командного рядка є числом >= 0."""
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("value must be integer") from error

    if number < 0:
        raise argparse.ArgumentTypeError("value must be >= 0")

    return number


def calculate_catalan_numbers(count):
    """Обчислити перші count чисел Каталана.

    Використовується ітеративна формула:
    C(n + 1) = C(n) * 2 * (2n + 1) / (n + 2)

    Такий підхід кращий, ніж окремо рахувати факторіали.
    """
    if count < 0:
        raise ValueError("count must be >= 0")

    if count == 0:
        return []

    numbers = [1]

    for index in range(count - 1):
        previous = numbers[-1]
        next_number = previous * 2 * (2 * index + 1) // (index + 2)
        numbers.append(next_number)

    return numbers


def is_prime(number):
    """Перевірити, чи є число простим."""
    if number < 2:
        return False

    if number == 2:
        return True

    if number % 2 == 0:
        return False

    limit = int(math.sqrt(number)) + 1

    for divisor in range(3, limit, 2):
        if number % divisor == 0:
            return False

    return True


def calculate_prime_numbers(count):
    """Обчислити перші count простих чисел."""
    if count < 0:
        raise ValueError("count must be >= 0")

    primes = []
    number = 2

    while len(primes) < count:
        if is_prime(number):
            primes.append(number)

        number += 1

    return primes


class CatalanThread(threading.Thread):
    """Потік для обчислення чисел Каталана."""

    def __init__(self, count):
        super().__init__()
        self.count = count
        self.result = []
        self.error = None

    def run(self):
        """Запустити обчислення у додатковому потоці."""
        try:
            self.result = calculate_catalan_numbers(self.count)
        except ValueError as error:
            self.error = error


class PrimeThread(threading.Thread):
    """Потік для обчислення простих чисел."""

    def __init__(self, count):
        super().__init__()
        self.count = count
        self.result = []
        self.error = None

    def run(self):
        """Запустити обчислення у додатковому потоці."""
        try:
            self.result = calculate_prime_numbers(self.count)
        except ValueError as error:
            self.error = error


def run_calculations(catalan_count, prime_count):
    """Запустити два потоки і повернути результати обчислень."""
    catalan_thread = CatalanThread(catalan_count)
    prime_thread = PrimeThread(prime_count)

    catalan_thread.start()
    prime_thread.start()

    catalan_thread.join()
    prime_thread.join()

    if catalan_thread.error is not None:
        raise catalan_thread.error

    if prime_thread.error is not None:
        raise prime_thread.error

    return catalan_thread.result, prime_thread.result


def build_parser():
    """Створити argparse-парсер для третього завдання."""
    parser = argparse.ArgumentParser(
        description="Threaded Catalan and prime numbers calculator"
    )

    parser.add_argument(
        "--catalan-count",
        type=non_negative_int,
        default=10,
        help="Number of Catalan numbers to calculate",
    )

    parser.add_argument(
        "--prime-count",
        type=non_negative_int,
        default=10,
        help="Number of prime numbers to calculate",
    )

    return parser


def main(argv=None):
    """Точка входу для запуску третього завдання."""
    parser = build_parser()
    args = parser.parse_args(argv)

    catalan_numbers, prime_numbers = run_calculations(
        args.catalan_count,
        args.prime_count,
    )

    print("Catalan numbers:")
    print(catalan_numbers)

    print("Prime numbers:")
    print(prime_numbers)


if __name__ == "__main__":
    main()
