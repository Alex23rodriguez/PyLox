from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.scanner import Token


class Expr(ABC):
    pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class Grouping(Expr):
    expression: Expr


@dataclass
class Literal(Expr):
    value: float | str | bool | None


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr
