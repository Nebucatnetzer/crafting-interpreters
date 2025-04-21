import argparse
import sys

from lox import Lox


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="LoxRepl",
        description="A REPL for the Lox language.",
    )
    parser.add_argument("--filename", default=None, required=False)
    return parser.parse_args(args)


def main() -> None:
    args = parse_args(sys.argv[1:])
    lox = Lox()
    lox.main(args)


if __name__ == "__main__":
    main()
