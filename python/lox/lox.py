import sys
from argparse import Namespace
from pathlib import Path


class Lox:
    def main(self, args: Namespace) -> None:
        if args.filename:
            self.__run_file(args.filename)
        self.__run_prompt()

    def __run_file(self, path: Path) -> None:
        with Path.open(path, "r") as file:
            print(file.read())

    def __run_prompt(self) -> None:
        print("prompt")
