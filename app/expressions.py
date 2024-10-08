from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from app.classes import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor) -> Any:
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)


@dataclass
class Literal(Expr):
    value: float | str | bool | None

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)
