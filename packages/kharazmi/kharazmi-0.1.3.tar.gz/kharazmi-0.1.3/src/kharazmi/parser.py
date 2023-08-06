from typing import NoReturn, Optional
from sly import Parser

from .types import ListFactory

from .exceptions import ParseError
from .models import BaseExpression, ContainsExpression, ListExpression, ListItems, NotContainsExpression, Text, Boolean, Variable, Number, IfExpression, FunctionExpression, FunctionArguments, LengthExpression
from .lexer import EquationLexer


class EquationParser(Parser):
    """
    EquationParser implements a CFG parser for the following grammar:

    expression    : expression + expression
                  | expression - expression
                  | expression * expression
                  | expression / expression
                  | expression ^ expression
                  | expression && expression
                  | expression || expression
                  | expression == expression
                  | expression != expression
                  | expression < expression
                  | expression <= expression
                  | expression > expression
                  | expression >= expression
                  | expression IN expression
                  | expression NOT_IN expression
                  | IF expression THEN expression ELSE expression.
                  | LENGTH_OF expression
                  | - expression
                  | ! expression
                  | ( expression )
                  | function_call
                  | variable
                  | list
                  | TEXT
                  | NUMBER
                  | TRUE
                  | FALSE

    function_call : IDENTIFIER ( arguments )

    variable      : IDENTIFIER

    arguments     : expression
                  | arguments , expression

    list          : [ list_items ]
    list_items    : expression
                  | list_items , expression
    """

    def __init__(self, list_factory: ListFactory):
        self._lexer = EquationLexer()
        self._list_factory = list_factory

    def parse(self, inp: str) -> Optional[BaseExpression]:
        tokens = [t for t in self._lexer.tokenize(inp)]
        print(tokens)
        return super().parse(iter(tokens))

    tokens = EquationLexer.tokens

    precedence = (
        ("right", LENGTH_OF),
        ("left", PLUS, MINUS),
        ("left", TIMES, DIVIDE),
        ("left", POWER),
        ('left', EQUAL, NOT_EQUAL, LESS_THAN, GREATER_THAN, LESS_THAN_OR_EQUAL, GREATER_THAN_OR_EQUAL, IN, NOT_IN),
        ('left', OR),
        ('left', AND),
        ('right', NOT),
        ('right', UMINUS),
    )

    start = 'expression'

    @_("expression PLUS expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 + p.expression1

    @_("expression MINUS expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 - p.expression1

    @_("expression TIMES expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 * p.expression1

    @_("expression DIVIDE expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 / p.expression1

    @_("expression POWER expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 ** p.expression1

    @_("expression AND expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 & p.expression1

    @_("expression OR expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 | p.expression1

    @_("expression EQUAL expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 == p.expression1

    @_("expression NOT_EQUAL expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 != p.expression1

    @_("expression GREATER_THAN expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 > p.expression1

    @_("expression GREATER_THAN_OR_EQUAL expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 >= p.expression1

    @_("expression LESS_THAN expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 < p.expression1

    @_("expression LESS_THAN_OR_EQUAL expression")
    def expression(self, p) -> BaseExpression:
        return p.expression0 <= p.expression1

    @_("expression IN expression")
    def expression(self, p) -> BaseExpression:
        return ContainsExpression(p.expression0, p.expression1)

    @_("expression NOT_IN expression")
    def expression(self, p) -> BaseExpression:
        return NotContainsExpression(p.expression0, p.expression1)

    @_("IF expression THEN expression ELSE expression '.'")
    def expression(self, p) -> BaseExpression:
        return IfExpression(p.expression0, p.expression1, p.expression2)

    @_("LENGTH_OF expression")
    def expression(self, p) -> BaseExpression:
        return LengthExpression(p.expression)

    @ _("MINUS expression %prec UMINUS")
    def expression(self, p) -> BaseExpression:
        return -p.expression

    @ _("NOT expression")
    def expression(self, p) -> BaseExpression:
        return ~p.expression

    @_("'(' expression ')'")
    def expression(self, p) -> BaseExpression:
        return p.expression

    @_("function_call")
    def expression(self, p) -> BaseExpression:
        return p.function_call

    @_("variable")
    def expression(self, p) -> BaseExpression:
        return p.variable

    @_("list")
    def expression(self, p) -> BaseExpression:
        return p.list

    @ _("TEXT")
    def expression(self, p) -> BaseExpression:
        return Text(p.TEXT)

    @ _("NUMBER")
    def expression(self, p) -> BaseExpression:
        return Number(p.NUMBER)

    @ _("TRUE")
    def expression(self, p) -> BaseExpression:
        return Boolean(True)

    @ _("FALSE")
    def expression(self, p) -> BaseExpression:
        return Boolean(False)

    @ _("IDENTIFIER '(' arguments ')'")
    def function_call(self, p) -> FunctionExpression:
        return FunctionExpression(p.IDENTIFIER, p.arguments)

    @_("IDENTIFIER")
    def variable(self, p) -> Variable:
        return Variable(p.IDENTIFIER)

    @ _("expression")
    def arguments(self, p) -> FunctionArguments:
        return FunctionArguments(p.expression)

    @ _("arguments ',' expression")
    def arguments(self, p) -> FunctionArguments:
        return p.arguments.append(p.expression)

    @ _("'[' list_items ']'")
    def list(self, p) -> ListExpression:
        return ListExpression(p.list_items)

    @ _("expression")
    def list_items(self, p) -> ListItems:
        return ListItems(self._list_factory, p.expression)

    @ _("list_items ',' expression")
    def list_items(self, p) -> ListItems:
        return p.list_items.append(p.expression)

    def error(self, p) -> NoReturn:
        if p is None:
            raise ParseError(f"Incomplete expression.")

        raise ParseError(f"Invalid expression. Error occurred in position {p.index}")
