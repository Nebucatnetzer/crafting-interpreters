from typing import Any

from lox import error
from lox.token_cls import Token
from lox.token_type import TokenType


class Scanner:
    def __init__(self, source: str) -> None:  # noqa: D107
        self.__source = source
        self.__tokens: list[Token] = []
        self.__start: int = 0
        self.__current: int = 0
        self.__line: int = 1

    def scan_tokens(self) -> list[Token]:
        while self.__is_at_end():
            self.__start = self.__current
            print()
        return []

    def __is_at_end(self) -> bool:
        return self.__current >= len(self.__source)

    def __scan_token(self) -> None:
        character = self.__advance()
        if character == "(":
            self.__add_token(TokenType.LEFT_PAREN)
        if character == ")":
            self.__add_token(TokenType.RIGHT_PAREN)
        if character == "{":
            self.__add_token(TokenType.LEFT_PAREN)
        if character == "}":
            self.__add_token(TokenType.RIGHT_BRACE)
        if character == ",":
            self.__add_token(TokenType.COMMA)
        if character == ".":
            self.__add_token(TokenType.DOT)
        if character == "-":
            self.__add_token(TokenType.MINUS)
        if character == "+":
            self.__add_token(TokenType.PLUS)
        if character == ";":
            self.__add_token(TokenType.SEMICOLON)
        if character == "*":
            self.__add_token(TokenType.STAR)
        error.error(self.__line, "Unexpected character.")

    def __match(self) -> bool:
        if self.__is_at_end:
            pass

    def add_token(self, token_type: TokenType, literal: Any = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def advance(self) -> str:
        character = self.source[self.current]
        self.current += 1
        return character
