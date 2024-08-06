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
        "=": "EQUAL",
        "==": "EQUAL_EQUAL",
        "!": "BANG",
        "!=": "BANG_EQUAL",
        "<": "LESS",
        ">": "GREATER",
        "<=": "LESS_EQUAL",
        ">=": "GREATER_EQUAL",
        "/": "SLASH",
    }

    skip = [" ", "\t"]

    failed = False

    for i, line in enumerate(lines):
        line = line.split("//", 1)[0]  # remove comments
        left = 0
        while left < len(line):
            right = left
            while right < len(line) and line[left : right + 1] in tokens:
                right += 1

            if left != right:
                t = line[left:right]
                print(f"{tokens[t]} {t} null")
                left = right
            elif line[left] in skip:
                left += 1
            else:
                failed = True
                print(f"line: {line}")
                print([ord(c) for c in line])
                print(
                    f"[line {i+1}] Error: Unexpected character: {line[left]}",
                    file=sys.stderr,
                )
                left += 1

    print("EOF  null")

    if failed:
        exit(65)


if __name__ == "__main__":
    main()
