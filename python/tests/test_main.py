from pathlib import Path

import lox
import pytest
from lox.__main__ import main
from lox.__main__ import parse_args
from lox.__main__ import run
from lox.__main__ import run_file
from lox.__main__ import run_prompt


def test_parse_args() -> None:
    inputs: list[str] = ["--filename", "README.md"]
    args = parse_args(args=inputs)
    assert args.filename == "README.md"


def test_run(capsys: pytest.CaptureFixture[str]) -> None:
    run("foo")
    output, _ = capsys.readouterr()
    assert "foo" in output


def test_prompt(capsys: pytest.CaptureFixture[str]) -> None:
    run_prompt()
    output, _ = capsys.readouterr()
    assert "> " in output


def test_file(capsys: pytest.CaptureFixture[str]) -> None:
    lox_script = Path("tests/example.lox")
    run_file(lox_script)
    output, _ = capsys.readouterr()
    assert "var" in output


def test_main(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Object:
        filename: Path

    def mock_args(_: list[str]) -> Object:

        args = Object()
        args.filename = Path("tests/example.lox")
        return args

    monkeypatch.setattr(lox.__main__, "parse_args", mock_args)

    main()
    output, _ = capsys.readouterr()
    assert "var" in output
