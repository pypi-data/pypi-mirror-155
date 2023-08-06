from typing import Union
from .parser import EquationParser


def main():
    parser = EquationParser(list_factory=lambda x: list(x))

    while True:
        cmd = input("> ")

        if check_for_exit(cmd):
            break

        expression = parser.parse(cmd)
        print(f"You've entered: {str(expression)}")
        if expression is None:
            raise RuntimeError("Sorry, we were not able to parse your expression.")

        print(f"You can do it in code using: {repr(expression)}")

        kwargs = {}

        for var in expression.variables:
            kwargs[var] = number_input(f"{var} = ")

        print(f"Result is: {expression.evaluate(**kwargs)}")


def number_input(message: str) -> Union[int, float, complex]:
    val = input(message)

    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return complex(val)


def check_for_exit(cmd: str) -> bool:
    return cmd.startswith("exit")


if __name__ == "__main__":
    main()
