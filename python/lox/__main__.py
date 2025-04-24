"""Main entry point of loxp."""

import argparse
import sys
from argparse import Namespace
from pathlib import Path

HAD_ERROR = False


def run(line: str) -> None:
    """Run lox line."""
    print(line)


def error(line: int, message: str) -> None:
    report(line, "", message)


def report(line: int, where: str, message: str) -> None:
    """Report an eror and it's location."""
    global HAD_ERROR  # noqa: PLW0603
    print("[line " + str(line) + "] Error" + where + ": " + message)
    HAD_ERROR = True


def run_file(path: Path) -> None:
    """Run the provided lox file, line by line."""
    with Path.open(path, "r") as file:
        for line in file.readlines():
            run(line)
            if HAD_ERROR:
                sys.exit(65)


def run_prompt() -> None:
    """Run the loxp REPL."""
    global HAD_ERROR  # noqa: PLW0603
    while True:
        user_input = input("> ")
        if not user_input:
            break
        run(user_input)
        HAD_ERROR = False


def parse_args(args: list[str]) -> Namespace:
    """Initialise the arguments."""
    parser = argparse.ArgumentParser(
        prog="LoxRepl",
        description="A REPL for the Lox language.",
    )
    parser.add_argument("--filename", default=None, required=False)
    return parser.parse_args(args)


def main() -> None:
    """Start loxp."""
    args = parse_args(sys.argv[1:])
    if args.filename:
        run_file(args.filename)
    else:
        run_prompt()


if __name__ == "__main__":
    main()
