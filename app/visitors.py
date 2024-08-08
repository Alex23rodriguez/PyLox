from abc import ABC, abstractmethod

from app.expressions import Binary, Expr, Grouping, Literal, Unary
from app.scanner import Token


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
        return f"({expr.operator.lexeme} {expr.accept(self)})"


class TokenParser(Visitor[Expr]):
    def visitBinaryExpr(self, expr):
        return Binary(expr.left.accept(self), expr.operator, expr.right.accept(self))

    def visitGroupingExpr(self, expr):
        return Grouping(expr.accept(self))

    def visitLiteralExpr(self, expr):
        return Literal(expr.value)

    def visitUnaryExpr(self, expr):
        return Unary(expr.operator, expr.right.accept(self))

    def parseTokens(self, tokens: list[Token]) -> Expr:

        # print(tokens)
        if len(tokens) == 1:
            return self._parse_literal(tokens[0])

        assert False, "can't parse this"

    def _parse_literal(self, token: Token):
        if token.type in [
            "NUMBER",
            "STRING",
        ]:
            return Literal(token.literal)
        elif token.type in [
            "TRUE",
            "FALSE",
            "NIL",
        ]:
            return Literal(token.lexeme)
        assert False, f"{token.type} can't be interpreted as a literal"
