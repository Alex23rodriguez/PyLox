from operator import add, eq, ge, gt, le, lt, mul, ne, sub, truediv

from app.expressions import Expr
from app.visitors import Visitor

operators = {
    "EQUAL_EQUAL": eq,
    "PLUS": add,
    "MINUS": sub,
    "STAR": mul,
    "BANG_EQUAL": ne,
    "LESS_EQUAL": le,
    "GREATER_EQUAL": ge,
    "LESS": lt,
    "GREATER": gt,
    "SLASH": truediv,
}


class Evaluator(Visitor):
    def evaluate(self, expr: Expr):
        return expr.accept(self)

    # overrides
    def visitBinaryExpr(self, expr):
        return operators[expr.operator.type](
            expr.left.accept(self), expr.right.accept(self)
        )

    def visitGroupingExpr(self, expr):
        return expr.expression.accept(self)

    def visitLiteralExpr(self, expr):
        return expr.value

    def visitUnaryExpr(self, expr):
        if expr.operator.type == "MINUS":
            return -expr.right.accept(self)
        else:
            return not expr.right.accept(self)
