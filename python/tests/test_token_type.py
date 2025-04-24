from lox.token_type import TokenType


def test_token_type_order() -> None:
    for token_type in TokenType:
        print(token_type.value)
    assert TokenType.LEFT_PAREN.value == 1
    assert TokenType.EOF.value == 39
