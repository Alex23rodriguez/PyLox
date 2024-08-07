import re
import sys


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


def evaluate(filename):
    with open(filename) as file:
        text = file.read().strip()

    if text in ["true", "false", "nil"]:
        print(text)


def tokenize(filename):
    with open(filename) as file:
        lines = file.readlines()

    tokens = {
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

    keys = ["\\" + k if k in special else k for k in tokens.keys()]
    token_pattern = re.compile(f"({'|'.join(keys)})")

    num_pattern = re.compile(r"[0-9]+(\.[0-9]+)?")
    str_pattern = re.compile('"(.*?)"')
    identifier_pattern = re.compile(r"[a-zA-Z_]\w*")
    whitespace_pattern = re.compile(r"\s+")

    failed = False
    for i, line in enumerate(lines, 1):
        while line:
            match line:
                # comment
                case s if s.startswith("//"):
                    break

                # token
                case s if m := token_pattern.match(s):
                    token = m.group()
                    print(f"{tokens[token]} {token} null")
                    line = line[m.end() :]

                # number
                case s if m := num_pattern.match(s):
                    num = m.group()
                    print(f"NUMBER {num} {float(num)}")
                    line = line[m.end() :]

                # string
                case s if m := str_pattern.match(s):
                    print(f"STRING {m.group()} {m.group(1)}")
                    line = line[m.end() :]

                # unterminated string
                case s if s.startswith('"'):
                    failed = True
                    print(
                        f"[line {i}] Error: Unterminated string.",
                        file=sys.stderr,
                    )
                    break

                # whitespace
                case s if m := whitespace_pattern.match(s):
                    line = line[m.end() :]

                # identifier or reserved
                case s if m := identifier_pattern.match(s):
                    w = m.group()
                    if w in reserved_words:
                        print(f"{w.upper()} {m.group()} null")
                    else:
                        print(f"IDENTIFIER {m.group()} null")
                    line = line[m.end() :]

                # bad token
                case _:
                    failed = True
                    print(
                        f"[line {i}] Error: Unexpected character: {line[0]}",
                        file=sys.stderr,
                    )
                    line = line[1:]
    print("EOF  null")

    if failed:
        exit(65)


if __name__ == "__main__":
    main()
