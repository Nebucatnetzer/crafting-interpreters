import argparse

from lox import Lox


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="LoxRepl",
        description="A REPL for the Lox language.",
    )
    parser.add_argument("--filename", default=None, required=False)
    args = parser.parse_args()
    lox = Lox()
    lox.main(args)


if __name__ == "__main__":
    main()
