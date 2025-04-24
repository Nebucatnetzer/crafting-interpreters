from lox.token_cls import Token
from lox.token_type import TokenType


def test_token_cls_init() -> None:
    token = Token(token_type=TokenType.AND, lexeme="and", literal="", line=20)
    assert token.lexeme == "and"
    assert token.token_type == TokenType.AND
    assert token.line == 20
