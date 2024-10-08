from typing import Literal as LiteralType

TokenType = LiteralType[
    "NUMBER",
    "STRING",
    "IDENTIFIER",
    "RIGHT_PAREN",
    "LEFT_PAREN",
    "RIGHT_BRACE",
    "LEFT_BRACE",
    "DOT",
    "COMMA",
    "SEMICOLON",
    "PLUS",
    "MINUS",
    "STAR",
    "EQUAL_EQUAL",
    "EQUAL",
    "BANG_EQUAL",
    "BANG",
    "LESS_EQUAL",
    "GREATER_EQUAL",
    "LESS",
    "GREATER",
    "SLASH",
    "AND",
    "CLASS",
    "ELSE",
    "FALSE",
    "FOR",
    "FUN",
    "IF",
    "NIL",
    "OR",
    "PRINT",
    "RETURN",
    "SUPER",
    "THIS",
    "TRUE",
    "VAR",
    "WHILE",
    "EOF",
]

BASIC_TOKENS: dict[str, TokenType] = {
    ")": "RIGHT_PAREN",
    "(": "LEFT_PAREN",
    "}": "RIGHT_BRACE",
    "{": "LEFT_BRACE",
    ".": "DOT",
    ",": "COMMA",
    ";": "SEMICOLON",
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "==": "EQUAL_EQUAL",
    "=": "EQUAL",
    "!=": "BANG_EQUAL",
    "!": "BANG",
    "<=": "LESS_EQUAL",
    ">=": "GREATER_EQUAL",
    "<": "LESS",
    ">": "GREATER",
    "/": "SLASH",
}
SPECIAL_REGEX = "().+*"

RESERVED_WORDS: dict[str, TokenType] = {
    "and": "AND",
    "class": "CLASS",
    "else": "ELSE",
    "false": "FALSE",
    "for": "FOR",
    "fun": "FUN",
    "if": "IF",
    "nil": "NIL",
    "or": "OR",
    "print": "PRINT",
    "return": "RETURN",
    "super": "SUPER",
    "this": "THIS",
    "true": "TRUE",
    "var": "VAR",
    "while": "WHILE",
}
