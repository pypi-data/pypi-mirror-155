class KharazmiBaseError(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class ParseError(KharazmiBaseError):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class EvaluationError(KharazmiBaseError):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class LexError(ParseError):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)
