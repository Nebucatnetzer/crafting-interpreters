from lox.token_cls import Token
from lox.token_type import TokenType

HAD_ERROR = False


class ParserError(Exception):
    def __init__(self, token: Token, message: str) -> None:
        self.token = token
        self.message = message
        super().__init__(self.message)
        error(line=self.token.line, token=self.token, message=self.message)


def error(line: int, token: None | Token = None, message: str = "") -> None:
    if token is None:
        report(line, "", message)
    elif token.token_type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at {token.lexeme}", message)


def report(line: int, where: str, message: str) -> None:
    """Report an eror and it's location."""
    global HAD_ERROR  # noqa: PLW0603
    print("[line " + str(line) + "] Error" + where + ": " + message)
    HAD_ERROR = True
