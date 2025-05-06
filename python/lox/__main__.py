"""Main entry point of loxp."""

import argparse
import sys
from argparse import Namespace
from pathlib import Path

from lox import error
from lox.ast_printer import AstPrinter
from lox.token_parser import Parser
from lox.scanner import Scanner


def run(line: str) -> None:
    """Run lox line."""
    ast_printer = AstPrinter()
    scanner = Scanner(line)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    expression = parser.parse()
    if error.HAD_ERROR:
        return
    print(ast_printer.print(expression))


def run_file(path: Path) -> None:
    """Run the provided lox file, line by line."""
    with Path.open(path, "r") as file:
        for line in file.readlines():
            run(line)
            if error.HAD_ERROR:
                sys.exit(65)


def run_prompt() -> None:
    """Run the loxp REPL."""
    while True:
        user_input = input("> ")
        if not user_input:
            break
        run(user_input)
        error.HAD_ERROR = False


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
