from typing import Union

from wa_typechecker import typechecked

from .Errors import LangSyntaxError
from .Expression import Expression


class Field:
    """A field in the interpolation. See details in package description.
    """
    @typechecked
    def __init__(self, src: Union[str, Expression]):
        if isinstance(src, Expression):
            self.__expr = src
        else:
            self.__expr = parse_field(src)

    @property
    @typechecked
    def expression(self) -> Expression:
        return self.__expr

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.__expr == other.__expr
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__expr)

    def __str__(self):
        return "{" + str(self.expression) + "}"

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(str(self))})"


@typechecked
def parse_field(src: str) -> Expression:
    """Parse a field and return a corresponding expression

    Tests:
    >>> parse_field("{reg14}")
    Identifier('reg14')
    >>> parse_field("{lad/lass}")
    Binary('lad/lass')
    >>> parse_field("reg14")
    Traceback (most recent call last):
    wa_language.syntax.Errors.LangSyntaxError: ...
    >>> parse_field("{x?x?x}")
    Traceback (most recent call last):
    wa_language.syntax.Errors.LangSyntaxError: ...
    """
    if src[0] != "{" or src[-1] != "}":
        raise LangSyntaxError("Not a field: " + repr(src))
    expr = src[1:-1]
    from .expression_parser import parse_expression
    return parse_expression(expr)


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)


