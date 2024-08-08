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
        assert tokens, "can't parse empty list"

        if len(tokens) == 1:
            return self._parse_literal(tokens[0])
        if len(tokens) == 2:
            return self._parse_unary(tokens)
        if tokens[0].type == "LEFT_PAREN":
            group, tokens = self._parse_parentheses(tokens)
            if not tokens:
                return group

            return self._parse_binary(group, tokens[0], tokens[1:])

        # TODO: what if first symbol is a unary operator?
        return self._parse_binary(self._parse_literal(tokens[0]), tokens[1], tokens[2:])

        # assert False, "can't parse this"

    def _parse_literal(self, token: Token) -> Literal:
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

    def _parse_unary(self, tokens: list[Token]) -> Unary:
        assert tokens[0].type in [
            "MINUS",
            "BANG",
        ], f"{tokens[0].type} can't be interpreted as unary operator"
        return Unary(tokens[0], self._parse_literal(tokens[1]))

    def _parse_parentheses(self, tokens: list[Token]) -> tuple[Grouping, list[Token]]:
        assert tokens[0].type == "LEFT_PAREN", "not a groupped expression"
        level = 0
        for i, t in enumerate(tokens[1:], 1):
            if t.type == "LEFT_PAREN":
                level += 1
            elif t.type == "RIGHT_PAREN":
                if level == 0:
                    return Grouping(self.parseTokens(tokens[1:i])), tokens[i + 1 :]
                level -= 1
        assert False, "Unmatched parentheses"

    def _parse_binary(self, left: Expr, op: Token, right: list[Token]) -> Binary:
        return Binary(left, op, self.parseTokens(right))
