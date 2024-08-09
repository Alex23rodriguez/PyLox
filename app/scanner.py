import re

from app.classes import Error, Token
from app.consts import BASIC_TOKENS, RESERVED_WORDS, SPECIAL_REGEX


def scan(text: str):
    lines = text.splitlines()

    keys = ["\\" + k if k in SPECIAL_REGEX else k for k in BASIC_TOKENS.keys()]
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
                    tokens.append(Token(BASIC_TOKENS[token], token, None, line_num))
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
                    if w in RESERVED_WORDS:
                        tokens.append(
                            Token(RESERVED_WORDS[w], m.group(), None, line_num)
                        )
                    else:
                        tokens.append(Token("IDENTIFIER", m.group(), None, line_num))
                    line = line[m.end() :]

                # bad token
                case _:
                    errors.append(Error(line_num, "Unexpected character: " + line[0]))
                    line = line[1:]
    tokens.append(Token("EOF", "", None, 0))

    return tokens, errors
