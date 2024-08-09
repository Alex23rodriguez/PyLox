from typing import Optional

from app.classes import Error, Token
from app.expressions import Binary, Expr, Grouping, Literal, Unary


class ParserError(Error):
    pass


class Parser:
    def parseTokens(
        self, tokens: list[Token]
    ) -> tuple[Optional[Expr], list[ParserError]]:
        if not tokens:
            return None, [ParserError(1, "", "Cannot parse empty token list")]
        try:
            expr, tokens = self.expression(tokens)
        except ParserError as e:
            return None, [e]

        if len(tokens) != 0:
            return None, [ParserError(0, " at end", "did not consume all tokens")]
        return expr, []

    def expression(self, tokens: list[Token]) -> tuple[Expr, list[Token]]:
        """given a list of tokens, return the expression they represent"""
        # top of grammar, lowest precedence
        expr, tokens = self.equality(tokens)
        return expr, tokens

    def equality(self, tokens: list[Token]) -> tuple[Expr, list[Token]]:
        """handle equality comparison"""
        expr, tokens = self.comparison(tokens)

        while tokens and tokens[0].type in [
            "BANG_EQUAL",
            "EQUAL_EQUAL",
        ]:
            op, *tokens = tokens
            right, tokens = self.comparison(tokens)
            expr = Binary(expr, op, right)

        return expr, tokens

    def comparison(self, tokens: list[Token]) -> tuple[Expr, list[Token]]:
        """handle <, >, <=, >= comparison"""
        expr, tokens = self.term(tokens)

        while tokens and tokens[0].type in [
            "LESS",
            "LESS_EQUAL",
            "GREATER",
            "GREATER_EQUAL",
        ]:
            op, *tokens = tokens
            right, tokens = self.term(tokens)
            expr = Binary(expr, op, right)

        return expr, tokens

    def term(self, tokens: list[Token]) -> tuple[Expr, list[Token]]:
        """handle +, -"""
        expr, tokens = self.factor(tokens)

        while tokens and tokens[0].type in ["PLUS", "MINUS"]:
            op, *tokens = tokens
            right, tokens = self.factor(tokens)
            expr = Binary(expr, op, right)

        return expr, tokens

    def factor(self, tokens: list[Token]) -> tuple[Expr, list[Token]]:
        """handle *, /"""
        expr, tokens = self.unary(tokens)

        while tokens and tokens[0].type in ["STAR", "SLASH"]:
            op, *tokens = tokens
            right, tokens = self.unary(tokens)
            expr = Binary(expr, op, right)

        return expr, tokens

    def unary(self, tokens: list[Token]) -> tuple[Expr, list[Token]]:
        """handle -, !"""
        if tokens and tokens[0].type in ["MINUS", "BANG"]:
            op, *tokens = tokens
            expr, tokens = self.unary(tokens)
            return Unary(op, expr), tokens

        return self.primary(tokens)

    def primary(self, tokens: list[Token]) -> tuple[Expr, list[Token]]:
        """handle literals and parentheses"""
        # bottom of grammar, highest precedence
        t, *tokens = tokens

        match t.type:
            case "NUMBER":
                assert t.literal is not None
                return Literal(float(t.literal)), tokens
            case "STRING":
                return Literal(t.literal), tokens
            case "TRUE":
                return Literal(True), tokens
            case "FALSE":
                return Literal(False), tokens
            case "NIL":
                return Literal(None), tokens
            case "LEFT_PAREN":
                return self._get_paren(tokens)
            case _:
                raise ParserError(t.line, "", "got non literal")

    def _get_paren(self, tokens: list[Token]):
        level = 0
        for i, t in enumerate(tokens):
            if t.type == "LEFT_PAREN":
                level += 1
            elif t.type == "RIGHT_PAREN":
                if level == 0:
                    expr, _ = self.expression(tokens[:i])
                    return (
                        Grouping(expr),
                        tokens[i + 1 :],
                    )
                level -= 1
        raise ParserError(-1, " at end", "Unmatched parentheses.")
