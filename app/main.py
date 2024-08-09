import sys

sys.path.append(".")

from app.evaluator import Evaluator
from app.parser import Parser
from app.scanner import scan
from app.visitors import AstPrinter


def tokenize(filename):
    with open(filename) as file:
        tokens, errors = scan(file.read())

    for token in tokens:
        print(token)

    for error in errors:
        error.report()

    if errors:
        exit(65)


def parse(filename):
    with open(filename) as file:
        tokens, errors = scan(file.read())

    if errors:
        exit(65)

    try:
        expr = Parser().parseTokens(tokens[:-1])
    except AssertionError as err:
        print(f"Error: {err}", file=sys.stderr)
        exit(65)

    print(AstPrinter().print(expr))


def evaluate(filename):
    with open(filename) as file:
        tokens, errors = scan(file.read())

    if errors:
        exit(65)

    try:
        expr = Parser().parseTokens(tokens[:-1])
    except AssertionError as err:
        print(f"Error: {err}", file=sys.stderr)
        exit(65)

    ans = Evaluator().evaluate(expr)
    print(ans)


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

    elif command == "parse":
        parse(filename)

    elif command == "evaluate":
        evaluate(filename)

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
