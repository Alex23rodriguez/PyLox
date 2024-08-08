from app.expressions import Expr, Visitor


class AstPrinter(Visitor[str]):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    # overrides
    def visitBinaryExpr(self, expr):
        return f"({expr.operator} {expr.left.accept(self)} {expr.right.accept(self)})"

    def visitGroupingExpr(self, expr):
        return f"({expr.expression.accept(self)})"

    def visitLiteralExpr(self, expr):
        return "nil" if expr.value is None else str(expr.value)

    def visitUnaryExpr(self, expr):
        return f"({expr.operator.lexeme} {expr.accept(self)})"
