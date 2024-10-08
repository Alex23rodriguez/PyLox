from operator import add, eq, ge, gt, le, lt, mul, ne, sub, truediv

from app.classes import Error
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


class EvalError(Error):
    pass


class Evaluator(Visitor):
    def evaluate(self, expr: Expr) -> tuple[str, list[EvalError]]:

        try:
            value = expr.accept(self)
            match value:
                case None:
                    return "nil", []
                case True | False:
                    return str(value).lower(), []
                case _:
                    if isinstance(value, float) and int(value) == value:
                        return str(int(value)), []
                    return str(value), []
        except Exception as e:
            return "", [EvalError(0, "", str(e))]

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
