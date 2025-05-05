from lox import error
from lox.scanner import Scanner


def test_scanner_init() -> None:
    _ = Scanner(source="var a = 1;")


def test_scan_token() -> None:
    characters = "(){},.-+;*<>="
    for character in characters:
        scanner = Scanner(source=character)
        scanner.scan_token()
        assert scanner.tokens[0].lexeme == character


def test_scan_error() -> None:
    scanner = Scanner(source="&")
    scanner.scan_token()
    assert error.HAD_ERROR


def test_scan_match() -> None:
    scanner = Scanner(source="fo")
    assert scanner.match(expected="f")
    assert scanner.match(expected="o")
    assert not scanner.match(expected="o")


def test_scan_peek() -> None:
    scanner = Scanner(source="f")
    assert "f" == scanner.peek()
    scanner.advance()
    assert "\0" == scanner.peek()
