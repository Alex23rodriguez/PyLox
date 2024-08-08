from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.scanner import Token


class Visitor(ABC):
    @abstractmethod
    def visitBinaryExpr(self, expr):
        pass

    @abstractmethod
    def visitGroupingExpr(self, expr):
        pass

    @abstractmethod
    def visitLiteralExpr(self, expr):
        pass

    @abstractmethod
    def visitUnaryExpr(self, expr):
        pass


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
        visitor.visitBinaryExpr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor):
        visitor.visitGroupingExpr(self)


@dataclass
class Literal(Expr):
    value: float | str | bool | None

    def accept(self, visitor):
        visitor.visitLiteralExpr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor):
        visitor.visitUnaryExpr(self)
