from lox import error
from lox.scanner import Scanner
from lox.scanner import is_digit


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
    error.HAD_ERROR = False


def test_scan_comment() -> None:
    scanner = Scanner(source="// comment")
    scanner.scan_token()
    assert scanner.tokens == []
    assert not error.HAD_ERROR


def test_scan_match() -> None:
    scanner = Scanner(source="fo")
    assert scanner.match(expected="f")
    assert scanner.match(expected="o")
    assert not scanner.match(expected="o")


def test_scan_peek() -> None:
    scanner = Scanner(source="fo")
    assert "f" == scanner.peek()
    scanner.advance()
    assert "o" == scanner.peek()
    scanner.advance()
    assert "\0" == scanner.peek()


def test_scan_peek_next() -> None:
    scanner = Scanner(source="fo")
    assert "o" == scanner.peek_next()
    scanner.advance()
    assert "\0" == scanner.peek_next()


def test_is_digit() -> None:
    assert is_digit("100")
    assert not is_digit("-100")
