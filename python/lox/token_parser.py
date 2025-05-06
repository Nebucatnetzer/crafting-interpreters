from lox import expr
from lox.error import ParserError
from lox.token_cls import Token
from lox.token_type import TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.current: int = 0
        self.tokens = tokens

    def parse(self) -> expr.Expr | None:
        try:
            return self.expression()
        except ParserError:
            return None

    def equality(self) -> expr.Expr:
        expression: expr.Expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: expr.Expr = self.comparison()
            expression = expr.Binary(expression, operator, right)
        return expression

    def term(self) -> expr.Expr:
        expression: expr.Expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator: Token = self.previous()
            right: expr.Expr = self.factor()
            expression = expr.Binary(expression, operator, right)
        return expression

    def comparison(self) -> expr.Expr:
        expression: expr.Expr = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator: Token = self.previous()
            right: expr.Expr = self.term()
            expression = expr.Binary(expression, operator, right)
        return expression

    def factor(self) -> expr.Expr:
        expression: expr.Expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator: Token = self.previous()
            right: expr.Expr = self.unary()
            expression = expr.Binary(expression, operator, right)
        return expression

    def unary(self) -> expr.Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.previous()
            right: expr.Expr = self.unary()
            return expr.Unary(operator, right)
        return self.primary()

    def primary(self) -> expr.Expr:
        if self.match(TokenType.FALSE):
            return expr.Literal(value=False)
        if self.match(TokenType.TRUE):
            return expr.Literal(value=True)
        if self.match(TokenType.NIL):
            return expr.Literal(value=None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return expr.Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return expr.Grouping(expression)

        raise ParserError(self.peek(), "Expect expression.")

    def match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise ParserError(self.peek(), message)

    def expression(self) -> expr.Expr:
        return self.equality()

    def synchonize(self) -> None:
        self.advance()
        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return
            match self.peek().token_type:
                case [
                    TokenType.CLASS,
                    TokenType.FUN,
                    TokenType.VAR,
                    TokenType.FOR,
                    TokenType.IF,
                    TokenType.WHILE,
                    TokenType.PRINT,
                    TokenType.RETURN,
                ]:
                    return
            self.advance()
