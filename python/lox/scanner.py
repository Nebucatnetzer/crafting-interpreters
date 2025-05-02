from typing import Any

from lox import error
from lox.token_cls import Token
from lox.token_type import TokenType


class Scanner:
    def __init__(self, source: str) -> None:  # noqa: D107
        self.source = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> list[Token]:
        while self.is_at_end():
            self.start = self.current
            print()
        return []

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        character = self.advance()
        if character == "(":
            self.add_token(TokenType.LEFT_PAREN)
        if character == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        if character == "{":
            self.add_token(TokenType.LEFT_PAREN)
        if character == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        if character == ",":
            self.add_token(TokenType.COMMA)
        if character == ".":
            self.add_token(TokenType.DOT)
        if character == "-":
            self.add_token(TokenType.MINUS)
        if character == "+":
            self.add_token(TokenType.PLUS)
        if character == ";":
            self.add_token(TokenType.SEMICOLON)
        if character == "*":
            self.add_token(TokenType.STAR)
        if character == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        error.error(self.line, "Unexpected character.")

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def add_token(self, token_type: TokenType, literal: Any = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def advance(self) -> str:
        character = self.source[self.current]
        self.current += 1
        return character
