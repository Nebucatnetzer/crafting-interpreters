from lox import expr
from lox.visitor import Visitor


class AstPrinter(Visitor):
    def print(self, expression: expr.Expr) -> object:
        return expression.accept(self)

    def visit_binary_expr(self, expression: expr.Binary) -> object:
        return parenthesize(
            expression.operator.lexeme, expression.left, expression.right
        )

    def visit_group_expr(self, expression: expr.Grouping) -> object:
        return parenthesize("group", expression.expression)

    def visit_literal_expr(self, expression: expr.Literal) -> object:
        if expression.value == None:
            return "nil"
        return str(expression.value)

    def visit_unary_expr(self, expression: expr.Unary) -> str:
        return parenthesize(expression.operator.lexeme, expression.right)

    def visit_assign_expr(self):
        pass

    def visit_expression_stmt(self):
        pass

    def visit_grouping_expr(self):
        pass

    def visit_print_stmt(self):
        pass

    def visit_var_stmt(self):
        pass

    def visit_variable_expr(self):
        pass


def parenthesize(name: str, *expressions: expr.Expr) -> str:
    builder = "(" + name
    for expression in expressions:
        builder.join(" " + expression.accept())
    builder.join(")")
    return builder
