from app.expressions import Binary, Expr, Grouping, Literal, Unary
from app.scanner import Token
from app.visitors import Visitor


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
        pass

    def expression(self, tokens: list[Token]) -> Expr:
        """given a list of tokens, return the expression they represent"""
        # top of grammar, lowest precedence
        pass

    def equality(self, tokens: list[Token]) -> Expr:
        """handle equality comparison"""
        pass

    def comparison(self, tokens: list[Token]) -> Expr:
        """handle <, >, <=, >= comparison"""
        pass

    def term(self, tokens: list[Token]) -> Expr:
        """handle +, -"""
        pass

    def factor(self, tokens: list[Token]) -> Expr:
        """handle *, /"""
        pass

    def unary(self, tokens: list[Token]) -> Expr:
        """handle -, !"""
        pass

    def primary(self, tokens: list[Token]) -> Expr:
        """handle literals and parentheses"""
        # bottom of grammar, highest precedence
        pass
