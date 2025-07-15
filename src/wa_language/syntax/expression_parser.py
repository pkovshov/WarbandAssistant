from typeguard import typechecked

from .Errors import LangSyntaxError
from .Binary import Binary
from .Expression import Expression
from .Identifier import Identifier
from .Ternary import Ternary


@typechecked
def parse_expression(expr: str) -> Expression:
    try:
        return Identifier(expr)
    except LangSyntaxError:
        pass
    try:
        return Binary(expr)
    except LangSyntaxError:
        pass
    try:
        return Ternary(expr)
    except LangSyntaxError:
        pass
    raise LangSyntaxError("Not an expression: " + repr(expr))
