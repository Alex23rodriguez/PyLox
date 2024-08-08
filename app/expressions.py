from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from app.scanner import Token


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
