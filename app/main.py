import sys

sys.path.append(".")

from app.evaluator import Evaluator
from app.parser import Parser
from app.scanner import scan
from app.visitors import AstPrinter


def tokenize(filename, log=True):
    with open(filename) as file:
        tokens, errors = scan(file.read())

    if log:
        for token in tokens:
            print(token)

    for error in errors:
        error.report()

    if errors:
        exit(65)

    return tokens


def parse(filename, log=True):
    tokens = tokenize(filename, log=False)
    expr, errors = Parser().parseTokens(tokens)

    for error in errors:
        error.report()

    if errors or expr is None:
        exit(65)

    if log:
        print(AstPrinter().print(expr))

    return expr


def evaluate(filename, log=True):
    expr = parse(filename, log=False)

    ans, errors = Evaluator().evaluate(expr)
    for error in errors:
        error.report()
    if errors or expr is None:
        exit(65)

    if log:
        print(ans)

    return ans


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
