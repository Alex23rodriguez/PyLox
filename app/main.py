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
    }

    failed = False

    for i, line in enumerate(lines):
        left = 0
        while left < len(line):
            right = left + 1
            token = None
            while right <= len(line) and (t := line[left:right]) in tokens:
                token = tokens[t]
                right += 1

            if token:
                print(f"{token} {line[left : right]} null")
            else:
                failed = True
                print(
                    f"[line {i+1}] Error: Unexpected character: {line[left]}",
                    file=sys.stderr,
                )

            left = right

    print("EOF  null")

    if failed:
        exit(65)


if __name__ == "__main__":
    main()
