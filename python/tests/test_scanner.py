from lox import error
from lox.scanner import Scanner


def test_scanner_init() -> None:
    _ = Scanner(source="var a = 1;")


def test_scan_token() -> None:
    characters = "(){},.-+;*"
    for character in characters:
        scanner = Scanner(source=character)
        scanner._Scanner__scan_token()
        assert scanner._Scanner__tokens[0].lexeme == character


def test_scan_error() -> None:
    scanner = Scanner(source="&")
    scanner._Scanner__scan_token()
    assert error.HAD_ERROR
