from pathlib import Path

import pytest
from lox import Lox


def test_lox_init() -> None:
    _ = Lox()


def test_lox_prompt(capsys: pytest.CaptureFixture[str]) -> None:
    lox_class = Lox()

    class Object:
        filename: Path | None

    args = Object()
    args.filename = None

    lox_class.main(args)
    output, _ = capsys.readouterr()
    assert "prompt" in output


def test_lox_read_file(capsys: pytest.CaptureFixture[str]) -> None:
    lox_class = Lox()

    class Object:
        filename: Path

    args = Object()
    readme = Path("tests/example.lox")
    args.filename = readme.absolute()

    lox_class.main(args)
    output, _ = capsys.readouterr()
    assert "var" in output
