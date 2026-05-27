"""Головний файл для запуску всіх завдань лабораторної роботи №8."""

import argparse

from src.task1_my_lock import run_demo as run_lock_demo
from src.task2_file_reader import run_demo as run_file_demo
from src.task3_calculations import run_calculations
from src.task3_calculations import non_negative_int


def build_parser():
    """Створити головний argparse-парсер з підкомандами."""
    parser = argparse.ArgumentParser(
        description="Laboratory work 8: Python threads"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    task1_parser = subparsers.add_parser(
        "task1",
        help="Run MyLock pipe demo",
    )
    task1_parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay before releasing blocked thread",
    )

    task2_parser = subparsers.add_parser(
        "task2",
        help="Run file reader thread demo",
    )
    task2_parser.add_argument(
        "file_path",
        help="Path to file for reading",
    )

    task3_parser = subparsers.add_parser(
        "task3",
        help="Run threaded calculations demo",
    )
    task3_parser.add_argument(
        "--catalan-count",
        type=non_negative_int,
        default=10,
        help="Number of Catalan numbers",
    )
    task3_parser.add_argument(
        "--prime-count",
        type=non_negative_int,
        default=10,
        help="Number of prime numbers",
    )

    return parser


def main(argv=None):
    """Запустити потрібне завдання залежно від команди користувача."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "task1":
        run_lock_demo(delay=args.delay)

    elif args.command == "task2":
        run_file_demo(args.file_path)

    elif args.command == "task3":
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
