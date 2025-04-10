import sys
from argparse import Namespace
from pathlib import Path


class Lox:
    def main(self, args: Namespace) -> None:
        if args.filename:
            self.__run_file(args.filename)
        self.__run_prompt()

    def __run_file(self, path: Path) -> None:
        with open(path) as file:
            print(file.read())
        sys.exit(0)

    def __run_prompt(self) -> None:
        print("prompt")
        sys.exit(0)
