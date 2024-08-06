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

    skip = [" ", "\t", "\n"]

    failed = False

    for i, line in enumerate(lines, 1):
        line = line.split("//", 1)[0]  # remove comments
        left = 0
        while left < len(line):

            if line[left] == '"':
                end = line.find('"', left + 1)
                if end == -1:
                    print(
                        f"[line {i}] Error: Unterminated string.",
                        file=sys.stderr,
                    )
                    failed = True
                    break
                else:
                    string = line[left + 1 : end]
                    print(f'STRING "{string}" {string}')
                    left = end + 1
                continue

            elif line[left] in skip:
                left += 1
                continue

            right = left
            while right < len(line) and line[left : right + 1] in tokens:
                right += 1

            if left != right:
                t = line[left:right]
                print(f"{tokens[t]} {t} null")
                left = right

            else:
                failed = True
                print(
                    f"[line {i}] Error: Unexpected character: {line[left]}",
                    file=sys.stderr,
                )
                left += 1
                continue

    print("EOF  null")

    if failed:
        exit(65)


if __name__ == "__main__":
    main()
