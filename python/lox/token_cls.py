# noqa: D100
from typing import Any

from lox.token_type import TokenType


class Token:
    """A class holding information about a given token."""

    def __init__(  # noqa: D107
        self,
        token_type: TokenType,
        lexeme: str,
        literal: Any,  # noqa: ANN401 I don't this yet
        line: int,
    ) -> None:
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:  # noqa: D105
        return f"{self.token_type} {self.lexeme} {self.literal}"
