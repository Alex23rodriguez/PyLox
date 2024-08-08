from abc import ABC, abstractmethod

from app.expressions import Binary, Expr, Grouping, Literal, Unary


class Visitor[T](ABC):
    @abstractmethod
    def visitBinaryExpr(self, expr: Binary) -> T:
        pass

    @abstractmethod
    def visitGroupingExpr(self, expr: Grouping) -> T:
        pass

    @abstractmethod
    def visitLiteralExpr(self, expr: Literal) -> T:
        pass

    @abstractmethod
    def visitUnaryExpr(self, expr: Unary) -> T:
        pass


class AstPrinter(Visitor[str]):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    # overrides
    def visitBinaryExpr(self, expr):
        return f"({expr.operator.lexeme} {expr.left.accept(self)} {expr.right.accept(self)})"

    def visitGroupingExpr(self, expr):
        return f"(group {expr.expression.accept(self)})"

    def visitLiteralExpr(self, expr):
        return "nil" if expr.value is None else str(expr.value)

    def visitUnaryExpr(self, expr):
        return f"({expr.operator.lexeme} {expr.right.accept(self)})"
