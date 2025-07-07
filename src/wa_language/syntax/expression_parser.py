from typeguard import typechecked

from .Binary import Binary
from .Expression import Expression
from .Identifier import Identifier
from .Ternary import Ternary


@typechecked
def parse_expression(expr: str) -> Expression:
    try:
        return Identifier(expr)
    except ValueError:
        pass
    try:
        return Binary(expr)
    except ValueError:
        pass
    try:
        return Ternary(expr)
    except ValueError:
        pass
    raise ValueError("Not an expression: " + repr(expr))
