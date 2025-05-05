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
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        return []

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        character = self.advance()
        if character in (" ", "\r", "\t"):
            pass
        elif character == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif character == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif character == "{":
            self.add_token(TokenType.LEFT_PAREN)
        elif character == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif character == ",":
            self.add_token(TokenType.COMMA)
        elif character == ".":
            self.add_token(TokenType.DOT)
        elif character == "-":
            self.add_token(TokenType.MINUS)
        elif character == "+":
            self.add_token(TokenType.PLUS)
        elif character == ";":
            self.add_token(TokenType.SEMICOLON)
        elif character == "*":
            self.add_token(TokenType.STAR)
        elif character == "!":
            if self.match("="):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif character == "=":
            if self.match("="):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif character == "<":
            if self.match("="):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif character == ">":
            if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif character == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif character == "\n":
            self.line += 1
        elif '"':
            self.scan_string()
        else:
            error.error(self.line, "Unexpected character.")

    def scan_string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            error.error(self.line, "Unterminated string.")
        self.advance()
        value: str = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, literal=value)

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
