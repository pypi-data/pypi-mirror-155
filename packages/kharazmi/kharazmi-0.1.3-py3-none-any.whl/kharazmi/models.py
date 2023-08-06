from abc import ABC, abstractmethod
import functools
from operator import contains

from typing import Dict, List, Set

from .types import Function, ListFactory, SupportsArithmetic, SupportsBoolean, SupportsConditional, SupportsList, SupportsString, TypedValue


class BaseExpression(ABC):
    @abstractmethod
    def evaluate(self, **variables_values: TypedValue) -> TypedValue: ...

    @property
    @abstractmethod
    def variables(self) -> Set[str]: ...

    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def __str__(self) -> str: ...

    def __add__(self, operand: "BaseExpression") -> "BaseExpression":
        return AdditionExpression(self, operand)

    def __radd__(self, operand: "BaseExpression") -> "BaseExpression":
        return AdditionExpression(operand, self)

    def __sub__(self, operand: "BaseExpression") -> "BaseExpression":
        return SubtractionExpression(self, operand)

    def __rsub__(self, operand: "BaseExpression") -> "BaseExpression":
        return SubtractionExpression(operand, self)

    def __mul__(self, operand: "BaseExpression") -> "BaseExpression":
        return MultiplicationExpression(self, operand)

    def __rmul__(self, operand: "BaseExpression") -> "BaseExpression":
        return MultiplicationExpression(operand, self)

    def __truediv__(self, operand: "BaseExpression") -> "BaseExpression":
        return DivisionExpression(self, operand)

    def __rtruediv__(self, operand: "BaseExpression") -> "BaseExpression":
        return DivisionExpression(operand, self)

    def __pow__(self, operand: "BaseExpression") -> "BaseExpression":
        return ExponentiationExpression(self, operand)

    def __rpow__(self, operand: "BaseExpression") -> "BaseExpression":
        return ExponentiationExpression(operand, self)

    def __neg__(self) -> "BaseExpression":
        return NegativeExpression(self)

    def __lt__(self, operand: "BaseExpression") -> "BaseExpression":
        return LessThanExpression(self, operand)

    def __le__(self, operand: "BaseExpression") -> "BaseExpression":
        return LessThanOrEqualExpression(self, operand)

    def __gt__(self, operand: "BaseExpression") -> "BaseExpression":
        return GreaterThanExpression(self, operand)

    def __ge__(self, operand: "BaseExpression") -> "BaseExpression":
        return GreaterThanOrEqualExpression(self, operand)

    def __and__(self, operand: "BaseExpression") -> "BaseExpression":
        return AndExpression(self, operand)

    def __or__(self, operand: "BaseExpression") -> "BaseExpression":
        return OrExpression(self, operand)

    def __invert__(self) -> "BaseExpression":
        return NotExpression(self)

    def __eq__(self, operand: "BaseExpression") -> "BaseExpression":
        return EqualExpression(self, operand)

    def __ne__(self, operand: "BaseExpression") -> "BaseExpression":
        return NotEqualExpression(self, operand)


class Variable(BaseExpression):
    def __init__(self, name: str) -> None:
        self._name = name

    def evaluate(self, **variable_values: TypedValue) -> TypedValue:
        if self._name not in variable_values:
            raise ValueError(f"Variable `{self._name}` does not have a value!")

        return variable_values[self._name]

    @ property
    def variables(self) -> Set[str]:
        return {self._name}

    def __repr__(self) -> str:
        return f"Variable('{self._name}')"

    def __str__(self) -> str:
        return self._name


class FunctionExpression(BaseExpression):
    supported_functions: Dict[str, Function] = {}

    def __init__(self, name: str, argument: "FunctionArguments") -> None:
        self._name = name
        self._argument = argument

    def evaluate(self, **variable_values: TypedValue) -> TypedValue:
        if self._name not in self.supported_functions.keys():
            raise ValueError(f"Function `{self._name}` has not been defined!")

        return self.supported_functions[self._name](*self._argument.evaluate(**variable_values))

    @ property
    def variables(self) -> Set[str]:
        return self._argument.variables

    @ classmethod
    def register(cls, name: str, runner: Function) -> None:
        cls.supported_functions[name] = runner

    def __repr__(self) -> str:
        return f"Function('{self._name}', {repr(self._argument)})"

    def __str__(self) -> str:
        return f"{self._name}({str(self._argument)})"


register_function = FunctionExpression.register


class FunctionArguments(object):
    def __init__(self, *expression: BaseExpression) -> None:
        self._expressions = [*expression]

    def evaluate(self, **variable_values: TypedValue) -> List[TypedValue]:
        return [expression.evaluate(**variable_values) for expression in self._expressions]

    @ property
    def variables(self) -> Set[str]:
        return functools.reduce(lambda a, b: a.union(b), [expression.variables for expression in self._expressions])

    def append(self, op: BaseExpression) -> 'FunctionArguments':
        if not isinstance(op, BaseExpression):  # pyright: ignore ["reportUnnecessaryIsinstance"]
            raise NotImplementedError()

        if isinstance(op, FunctionArguments):
            return FunctionArguments(*self._expressions, *op._expressions)

        return FunctionArguments(*self._expressions, op)

    def __repr__(self) -> str:
        return f"FunctionArgument({', '.join([repr(expression) for expression in self._expressions])})"

    def __str__(self) -> str:
        return f"{', '.join([str(expression) for expression in self._expressions])}"


class ListExpression(BaseExpression):
    def __init__(self, items: "ListItems") -> None:
        self.items = items

    def evaluate(self, **variable_values: TypedValue) -> SupportsList:
        return self.items.evaluate(**variable_values)

    @ property
    def variables(self) -> Set[str]:
        return self.items.variables

    def __repr__(self) -> str:
        return f"ListExpression({repr(self.items)})"

    def __str__(self) -> str:
        return f"[ {str(self.items)} ]"


class ListItems(object):
    def __init__(self, list_factory: ListFactory, *expression: BaseExpression) -> None:
        self._expressions = [*expression]
        self._list_factory = list_factory

    def evaluate(self, **variable_values: TypedValue) -> SupportsList:
        return self._list_factory([expression.evaluate(**variable_values) for expression in self._expressions])

    @ property
    def variables(self) -> Set[str]:
        return functools.reduce(lambda a, b: a.union(b), [expression.variables for expression in self._expressions])

    def append(self, op: BaseExpression) -> 'ListItems':
        if not isinstance(op, BaseExpression):  # pyright: ignore ["reportUnnecessaryIsinstance"]
            raise NotImplementedError()

        return ListItems(self._list_factory, *self._expressions, op)

    def __repr__(self) -> str:
        return f"ListItems({', '.join([repr(expression) for expression in self._expressions])})"

    def __str__(self) -> str:
        return f"{', '.join([str(expression) for expression in self._expressions])}"


class BaseUnaryExpression(BaseExpression):
    def __init__(self, operand_expression: BaseExpression) -> None:
        self._operand_expression = operand_expression

    def evaluate(self, **variable_values: TypedValue) -> TypedValue:
        operand_value = self._operand_expression.evaluate(**variable_values)
        return self._apply(operand_value)

    @ property
    def variables(self) -> Set[str]:
        return self._operand_expression.variables

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._operand_expression)})"

    def __str__(self) -> str:
        return f"{self._operator_symbol}{str(self._operand_expression)}"

    @ property
    @ abstractmethod
    def _operator_symbol(self) -> str: ...

    @ abstractmethod
    def _apply(self, operand_value: TypedValue) -> TypedValue: ...


class BaseBinaryExpression(BaseExpression):
    def __init__(self, left_hand_side_expression: BaseExpression, right_hand_side_expression: BaseExpression) -> None:
        self._left_hand_side_expression = left_hand_side_expression
        self._right_hand_side_expression = right_hand_side_expression

    def evaluate(self, **variables_values: TypedValue) -> TypedValue:
        left_hand_side_value = self._left_hand_side_expression.evaluate(**variables_values)
        right_hand_side_value = self._right_hand_side_expression.evaluate(**variables_values)
        return self._apply(left_hand_side_value, right_hand_side_value)

    @ property
    def variables(self) -> Set[str]:
        return self._right_hand_side_expression.variables.union(self._left_hand_side_expression.variables)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._left_hand_side_expression)}, {repr(self._right_hand_side_expression)})"

    def __str__(self) -> str:
        return f"{str(self._left_hand_side_expression)} {self._operator_symbol} {str(self._right_hand_side_expression)}"

    @ property
    @ abstractmethod
    def _operator_symbol(self) -> str: ...

    @ abstractmethod
    def _apply(self, left_hand_side_value: TypedValue, right_hand_side_value: TypedValue) -> TypedValue: ...


class BaseTrinaryExpression(BaseExpression):
    def __init__(self, operand1_expression: BaseExpression, operand2_expression: BaseExpression, operand3_expression: BaseExpression) -> None:
        self._operand1_expression = operand1_expression
        self._operand2_expression = operand2_expression
        self._operand3_expression = operand3_expression

    def evaluate(self, **variable_values: TypedValue) -> TypedValue:
        operand1_value = self._operand1_expression.evaluate(**variable_values)
        operand2_value = self._operand2_expression.evaluate(**variable_values)
        operand3_value = self._operand3_expression.evaluate(**variable_values)
        return self._apply(operand1_value, operand2_value, operand3_value)

    @ property
    def variables(self) -> Set[str]:
        return self._operand1_expression.variables.union(self._operand2_expression.variables).union(self._operand3_expression.variables)

    @ abstractmethod
    def _apply(self, operand1_value: TypedValue, operand2_value: TypedValue,
               operand3_value: TypedValue) -> TypedValue: ...


class IfExpression(BaseTrinaryExpression):
    def __repr__(self) -> str:
        return f"IfExpression({repr(self._operand1_expression)}, {repr(self._operand2_expression)}, {repr(self._operand3_expression)})"

    def __str__(self) -> str:
        return f"{str(self._operand1_expression)}?{str(self._operand2_expression)}:{str(self._operand3_expression)}"

    def _apply(self, operand1_value: TypedValue, operand2_value: TypedValue, operand3_value: TypedValue) -> TypedValue:
        if isinstance(operand1_value, bool):
            return operand2_value if operand1_value else operand3_value

        if isinstance(operand1_value, SupportsConditional):
            return operand1_value._cond__(operand2_value, operand3_value)

        raise NotImplementedError("Conditional operation has not been implemented on the first operand.")


class LengthExpression(BaseUnaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "len "

    def _apply(self, value: "TypedValue") -> SupportsArithmetic:
        if not isinstance(value, SupportsString):
            raise ValueError("invalid arguments for - (negative) operation")

        return value.__len__()


class AdditionExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "+"

    def _apply(self, left_hand_side_value: "TypedValue", right_hand_side_value: "TypedValue") -> SupportsArithmetic | SupportsString | SupportsList:
        if isinstance(left_hand_side_value, SupportsArithmetic) and isinstance(right_hand_side_value, SupportsArithmetic):
            return left_hand_side_value + right_hand_side_value

        if isinstance(left_hand_side_value, SupportsString) and isinstance(right_hand_side_value, SupportsString):
            return left_hand_side_value + right_hand_side_value

        if isinstance(left_hand_side_value, SupportsList) and isinstance(right_hand_side_value, SupportsList):
            return left_hand_side_value + right_hand_side_value

        raise ValueError("invalid arguments for + operation (dose not supports arithmetic or string")


class SubtractionExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "-"

    def _apply(self, left_hand_side_value: "TypedValue", right_hand_side_value: "TypedValue") -> SupportsArithmetic:
        if not isinstance(left_hand_side_value, SupportsArithmetic) or not isinstance(right_hand_side_value, SupportsArithmetic):
            raise ValueError("invalid arguments for - operation")

        return left_hand_side_value - right_hand_side_value


class MultiplicationExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "*"

    def _apply(self, left_hand_side_value: "TypedValue", right_hand_side_value: "TypedValue") -> SupportsArithmetic:
        if not isinstance(left_hand_side_value, SupportsArithmetic) or not isinstance(right_hand_side_value, SupportsArithmetic):
            raise ValueError("invalid arguments for * operation")

        return left_hand_side_value * right_hand_side_value


class DivisionExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "/"

    def _apply(self, left_hand_side_value: "TypedValue", right_hand_side_value: "TypedValue") -> SupportsArithmetic:
        if not isinstance(left_hand_side_value, SupportsArithmetic) or not isinstance(right_hand_side_value, SupportsArithmetic):
            raise ValueError("invalid arguments for / operation")

        return left_hand_side_value / right_hand_side_value


class ExponentiationExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "^"

    def _apply(self, left_hand_side_value: "TypedValue", right_hand_side_value: "TypedValue") -> SupportsArithmetic:
        if not isinstance(left_hand_side_value, SupportsArithmetic) or not isinstance(right_hand_side_value, SupportsArithmetic):
            raise ValueError("invalid arguments for / operation")

        return left_hand_side_value ** right_hand_side_value


class NegativeExpression(BaseUnaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "-"

    def _apply(self, value: "TypedValue") -> SupportsArithmetic:
        if not isinstance(value, SupportsArithmetic):
            raise ValueError("invalid arguments for - (negative) operation")

        return -value


class EqualExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "=="

    def _apply(self, left_hand_side_value: "TypedValue", right_hand_side_value: "TypedValue") -> SupportsBoolean:
        if isinstance(left_hand_side_value, SupportsArithmetic) and isinstance(right_hand_side_value, SupportsArithmetic):
            return left_hand_side_value == right_hand_side_value

        if isinstance(left_hand_side_value, SupportsBoolean) and isinstance(right_hand_side_value, SupportsBoolean):
            return left_hand_side_value == right_hand_side_value

        if isinstance(left_hand_side_value, SupportsString) and isinstance(right_hand_side_value, SupportsString):
            return left_hand_side_value == right_hand_side_value

        if isinstance(left_hand_side_value, SupportsList) and isinstance(right_hand_side_value, SupportsList):
            return left_hand_side_value == right_hand_side_value

        raise ValueError("invalid arguments for EQUAL operation")


class NotEqualExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "!="

    def _apply(self, left_hand_side_value: "TypedValue", right_hand_side_value: "TypedValue") -> SupportsBoolean:
        if isinstance(left_hand_side_value, SupportsArithmetic) and isinstance(right_hand_side_value, SupportsArithmetic):
            return left_hand_side_value != right_hand_side_value

        if isinstance(left_hand_side_value, SupportsBoolean) and isinstance(right_hand_side_value, SupportsBoolean):
            return left_hand_side_value != right_hand_side_value

        if isinstance(left_hand_side_value, SupportsString) and isinstance(right_hand_side_value, SupportsString):
            return left_hand_side_value != right_hand_side_value

        if isinstance(left_hand_side_value, SupportsList) and isinstance(right_hand_side_value, SupportsList):
            return left_hand_side_value != right_hand_side_value

        raise ValueError("invalid arguments for NOT EQUAL operation")


class LessThanExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "<"

    def _apply(self, left_hand_side_value: "TypedValue", right_hand_side_value: "TypedValue") -> SupportsBoolean:
        if not isinstance(left_hand_side_value, SupportsArithmetic) or not isinstance(right_hand_side_value, SupportsArithmetic):
            raise ValueError("invalid arguments for < operation")

        return left_hand_side_value < right_hand_side_value


class LessThanOrEqualExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "<="

    def _apply(self, left_hand_side_value: "TypedValue", right_hand_side_value: "TypedValue") -> SupportsBoolean:
        if not isinstance(left_hand_side_value, SupportsArithmetic) or not isinstance(right_hand_side_value, SupportsArithmetic):
            raise ValueError("invalid arguments for <= operation")

        return left_hand_side_value <= right_hand_side_value


class GreaterThanExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return ">"

    def _apply(self, left_hand_side_value: "TypedValue", right_hand_side_value: "TypedValue") -> SupportsBoolean:
        if not isinstance(left_hand_side_value, SupportsArithmetic) or not isinstance(right_hand_side_value, SupportsArithmetic):
            raise ValueError("invalid arguments for > operation")

        return left_hand_side_value > right_hand_side_value


class GreaterThanOrEqualExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return ">="

    def _apply(self, left_hand_side_value: "TypedValue", right_hand_side_value: "TypedValue") -> SupportsBoolean:
        if not isinstance(left_hand_side_value, SupportsArithmetic) or not isinstance(right_hand_side_value, SupportsArithmetic):
            raise ValueError("invalid arguments for >= operation")

        return left_hand_side_value >= right_hand_side_value


class AndExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "AND"

    def _apply(self, left_hand_side_value: TypedValue, right_hand_side_value: TypedValue) -> SupportsBoolean:
        if isinstance(left_hand_side_value, bool) and isinstance(right_hand_side_value, bool):
            return left_hand_side_value and right_hand_side_value

        if not isinstance(left_hand_side_value, SupportsBoolean) or not isinstance(right_hand_side_value, SupportsBoolean):
            raise ValueError("invalid arguments for AND operation")

        return left_hand_side_value & right_hand_side_value


class OrExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "OR"

    def _apply(self, left_hand_side_value: TypedValue, right_hand_side_value: TypedValue) -> TypedValue:
        if isinstance(left_hand_side_value, bool) and isinstance(right_hand_side_value, bool):
            return left_hand_side_value or right_hand_side_value

        if not isinstance(left_hand_side_value, SupportsBoolean) or not isinstance(right_hand_side_value, SupportsBoolean):
            raise ValueError("invalid arguments for OR operation")

        return left_hand_side_value | right_hand_side_value


class NotExpression(BaseUnaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "NOT"

    def _apply(self, operand_value: TypedValue) -> TypedValue:
        if isinstance(operand_value, bool):
            return not operand_value

        if not isinstance(operand_value, SupportsBoolean):
            raise ValueError("invalid arguments for NOT operation")

        return ~operand_value


class ContainsExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "IN"

    def _apply(self, left_hand_side_value: TypedValue, right_hand_side_value: TypedValue) -> TypedValue:
        if not isinstance(right_hand_side_value, SupportsList):
            raise ValueError("invalid arguments for IN operation")

        return right_hand_side_value.__contains__(left_hand_side_value)


class NotContainsExpression(BaseBinaryExpression):
    @ property
    def _operator_symbol(self) -> str:
        return "NOT IN"

    def _apply(self, left_hand_side_value: TypedValue, right_hand_side_value: TypedValue) -> TypedValue:
        if not isinstance(right_hand_side_value, SupportsList):
            raise ValueError("invalid arguments for IN operation")

        contains = right_hand_side_value.__contains__(left_hand_side_value)

        if isinstance(contains, bool):
            return not contains

        return ~ contains


class Text(BaseExpression):
    def __init__(self, value: str) -> None:
        self._value = value

    def evaluate(self, **_: TypedValue) -> str:
        return self._value

    @ property
    def variables(self) -> Set[str]:
        return set()

    def __repr__(self):
        return f"Text('{repr(self._value)}')"

    def __str__(self):
        return str(self._value)


class Number(BaseExpression):
    def __init__(self, value: str) -> None:
        self._value: int | float | complex

        try:
            self._value = int(value)
        except ValueError:
            try:
                self._value = float(value)
            except ValueError:
                self._value = complex(value)

    def evaluate(self, **_: TypedValue) -> int | float | complex:
        return self._value

    @ property
    def variables(self) -> Set[str]:
        return set()

    def __repr__(self):
        return f"Number('{repr(self._value)}')"

    def __str__(self):
        return str(self._value)


class Boolean(BaseExpression):
    def __init__(self, value: bool) -> None:
        self._value = value

    def evaluate(self, **_: TypedValue) -> bool:
        return self._value

    @ property
    def variables(self) -> Set[str]:
        return set()

    def __repr__(self):
        return f"Boolean('{repr(self._value)}')"

    def __str__(self):
        return str(self._value)
