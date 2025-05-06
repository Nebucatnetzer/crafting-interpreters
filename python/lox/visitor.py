from abc import ABC, abstractmethod
from lox import expr
from lox import stmt


class Visitor(ABC):
    @abstractmethod
    def visit_assign_expr(self, expr: expr.Assign) -> object:
        pass

    @abstractmethod
    def visit_binary_expr(self, expr: expr.Binary) -> object:
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: expr.Grouping) -> object:
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: expr.Literal) -> object:
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: expr.Unary) -> object:
        pass

    @abstractmethod
    def visit_variable_expr(self, expr: expr.Variable) -> object:
        pass

    @abstractmethod
    def visit_expression_stmt(self, stmt: stmt.Expression) -> None:
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: stmt.Print) -> None:
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt: stmt.Var) -> None:
        pass
