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

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        lines = file.readlines()

    tokens = {
        "(": "LEFT_PAREN",
        ")": "RIGHT_PAREN",
        "{": "LEFT_BRACE",
        "}": "RIGHT_BRACE",
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

    failed = False
    token_pattern = re.compile(f"({'|'.join(tokens.keys())})")
    num_pattern = re.compile(r"[0-9]+(\.[0-9]+)?")
    str_pattern = re.compile('".*?"')
    whitespace_pattern = re.compile(r"\s+")

    for i, line in enumerate(lines, 1):
        while line:
            match line:
                # comment
                case s if s.startswith("//"):
                    break

                # token
                case s if m := token_pattern.match(s):
                    n = m.span()[1]
                    token = line[:n]
                    print(f"{tokens[token]} {token} null")
                    line = line[n:]

                # number
                case s if m := num_pattern.match(s):
                    n = m.span()[1]
                    num = line[:n]
                    print(f"NUMBER {num} {num if '.' in num else num + '.0'}")
                    line = line[n:]

                # string
                case s if m := str_pattern.match(s):
                    n = m.span()[1]
                    print(f'STRING "{s[:n]}" {s[1:n-1]}')
                    line = line[n:]

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
                    line = line[m.span()[1] :]

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
