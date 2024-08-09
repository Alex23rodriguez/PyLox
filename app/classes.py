import sys
from dataclasses import dataclass
from typing import Optional

from app.consts import TokenType


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: Optional[str]
    line: int

    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {'null' if self.literal is None else self.literal}"

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.lexeme}, {'null' if self.literal is None else self.literal})"


@dataclass
class Error:
    line: int
    message: str

    def report(self):
        print(f"[line {self.line}] Error: {self.message}", file=sys.stderr)
