import re
import sys
from typing import Optional


# CLASSES
class Token:
    def __init__(
        self, typ: str, lexeme: str, literal: Optional[str], line: int
    ) -> None:
        self.type = typ
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return (
            f"{self.type} {self.lexeme} {'null' if self.literal is None else self.line}"
        )


class Error:
    def __init__(self, line: int, message: str) -> None:
        self.line = line
        self.message = message

    def report(self):
        print(f"[line {self.line}] Error: {self.message}", file=sys.stderr)


# COMMANDS
def evaluate(filename):
    with open(filename) as file:
        text = file.read().strip()

    if text in ["true", "false", "nil"]:
        print(text)


def tokenize(filename):
    with open(filename) as file:
        tokens, errors = scan(file.read())

    for token in tokens:
        print(token)

    for error in errors:
        error.report()

    if errors:
        exit(65)


def scan(text: str):
    lines = text.splitlines()

    basic_tokens = {
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
    special = "().+*"

    reserved_words = [
        "and",
        "class",
        "else",
        "false",
        "for",
        "fun",
        "if",
        "nil",
        "or",
        "print",
        "return",
        "super",
        "this",
        "true",
        "var",
        "while",
    ]

    keys = ["\\" + k if k in special else k for k in basic_tokens.keys()]
    token_pattern = re.compile(f"({'|'.join(keys)})")

    num_pattern = re.compile(r"[0-9]+(\.[0-9]+)?")
    str_pattern = re.compile('"(.*?)"')
    identifier_pattern = re.compile(r"[a-zA-Z_]\w*")
    whitespace_pattern = re.compile(r"\s+")

    tokens: list[Token] = []
    errors: list[Error] = []
    for line_num, line in enumerate(lines, 1):
        while line:
            match line:
                # comment
                case s if s.startswith("//"):
                    break

                # token
                case s if m := token_pattern.match(s):
                    token = m.group()
                    tokens.append(Token(basic_tokens[token], token, None, line_num))
                    line = line[m.end() :]

                # number
                case s if m := num_pattern.match(s):
                    num = m.group()
                    tokens.append(Token("NUMBER", num, str(float(num)), line_num))
                    line = line[m.end() :]

                # string
                case s if m := str_pattern.match(s):
                    tokens.append(Token("STRING", m.group(), m.group(1), line_num))
                    line = line[m.end() :]

                # unterminated string
                case s if s.startswith('"'):
                    errors.append(Error(line_num, "Unterminated string."))
                    break

                # whitespace
                case s if m := whitespace_pattern.match(s):
                    line = line[m.end() :]

                # identifier or reserved
                case s if m := identifier_pattern.match(s):
                    w = m.group()
                    if w in reserved_words:
                        tokens.append(Token(w.upper(), m.group(), None, line_num))
                    else:
                        tokens.append(Token("IDENTIFIER", m.group(), None, line_num))
                    line = line[m.end() :]

                # bad token
                case _:
                    errors.append(Error(line_num, "Unexpected character: " + line[0]))
                    line = line[1:]
    tokens.append(Token("EOF", "", None, 0))

    return tokens, errors


# MAIN
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command == "tokenize":
        tokenize(filename)

    elif command == "evaluate":
        evaluate(filename)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
