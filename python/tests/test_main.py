from pathlib import Path

import pytest
from lox.__main__ import main
from lox.__main__ import parse_args
from lox.__main__ import run_file
from lox.__main__ import run_prompt


def test_parse_args() -> None:
    args = parse_args()


def test_prompt(capsys: pytest.CaptureFixture[str]) -> None:
    run_prompt()
    output, _ = capsys.readouterr()
    assert "prompt" in output


def test_file(capsys: pytest.CaptureFixture[str]) -> None:
    lox_script = Path("tests/example.lox")
    run_file(lox_script)
    output, _ = capsys.readouterr()
    assert "var" in output


def test_main(capsys: pytest.CaptureFixture[str]) -> None:
    class Object:
        filename: Path

    args = Object()
    readme = Path("tests/example.lox")
    args.filename = readme.absolute()

    main(args)
    output, _ = capsys.readouterr()
    assert "var" in output
