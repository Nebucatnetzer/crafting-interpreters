import argparse
import sys
from argparse import Namespace
from pathlib import Path


def run(line: str) -> None:
    print(line)


def run_file(path: Path) -> None:
    with Path.open(path, "r") as file:
        for line in file.readlines():
            run(line)


def run_prompt() -> None:
    while True:
        user_input = input("> ")
        if not user_input:
            break
        run(user_input)


def parse_args(args: list[str]) -> Namespace:
    parser = argparse.ArgumentParser(
        prog="LoxRepl",
        description="A REPL for the Lox language.",
    )
    parser.add_argument("--filename", default=None, required=False)
    return parser.parse_args(args)


def main() -> None:
    args = parse_args(sys.argv[1:])
    if args.filename:
        run_file(args.filename)
    else:
        run_prompt()


if __name__ == "__main__":
    main()
