from typing import Set
from sly import Lexer
from sly.lex import Token


from .exceptions import LexError


class EquationLexer(Lexer):
    tokens: Set[str] = {
        NUMBER,
        IDENTIFIER,
        PLUS,
        MINUS,
        TIMES,
        DIVIDE,
        POWER,
        EQUAL,
        NOT_EQUAL,
        GREATER_THAN,
        LESS_THAN,
        GREATER_THAN_OR_EQUAL,
        LESS_THAN_OR_EQUAL,
        AND,
        OR,
        NOT,
        TRUE,
        FALSE,
        IF,
        THEN,
        ELSE,
        TEXT,
        LENGTH_OF,
        IN,
        NOT_IN,
    }

    literals = ["(", ")", ",", ".", "[", "]"]
    ignore = " \t"

    # NOTE: ordering of tokens should be in a way that more specific tokens (e.g: IS LESS THAN) come before less specific ones (e.g: IS)

    @_(r"\d+(\.\d+)?((\+|\-)\d+(\.\d*)?j)?")
    def NUMBER(self, t):
        try:
            t.value = int(t.value)
        except ValueError:
            try:
                t.value = float(t.value)
            except ValueError:
                t.value = complex(t.value)

        return t

    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    POWER = r"\^"

    GREATER_THAN_OR_EQUAL = r"\>=|IS GREATER THAN OR EQUAL|is greater than or equal"
    GREATER_THAN = r"\>|IS GREATER THAN|is greater than"

    LESS_THAN_OR_EQUAL = r"\<=|IS LESS THAN OR EQUAL|is less than or equal"
    LESS_THAN = r"\<|IS LESS THAN|is less than"

    NOT_EQUAL = r"\!\=|IS NOT|is not"

    EQUAL = r"\=\=|IS|is"

    LENGTH_OF = r"length of|LENGTH OF"

    AND = r"\&\&|AND|and"
    OR = r"\|\||OR|or"
    NOT_IN = r"NOT IN|not in"
    NOT = r"\!|NOT|not"
    TRUE = r"true|TRUE|True"
    FALSE = r"false|FALSE|False"
    IF = r"if|IF"
    IN = r"in|IN"
    THEN = r"then|THEN"
    ELSE = r"else|ELSE"
    IDENTIFIER = r"[a-zA-Z_][a-zA-Z_0-9]*"

    @_(r"\".*?\"")
    def TEXT(self, t):
        t.value = t.value[1:-1]
        return t

    def error(self, token: Token):
        raise LexError(f"Invalid token '{token.value[0]}'")
