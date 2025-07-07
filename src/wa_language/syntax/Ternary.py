from typing import Tuple

from typeguard import typechecked

from .Expression import Expression
from .Identifier import Identifier
from .Interpolation import Interpolation


class Ternary(Expression):
    @typechecked
    def __init__(self, src: str):
        super().__init__()
        self.__items = parse_ternary(src)

    @property
    @typechecked
    def condition(self) -> Identifier:
        return self.__items[0]

    @property
    @typechecked
    def true_part(self) -> Interpolation:
        return self.__items[1]

    @property
    @typechecked
    def false_part(self) -> Interpolation:
        return self.__items[2]

    def _extract_variables(self):
        condition_variables = self.condition.variables
        true_part_variables = self.true_part.variables
        false_part_variables = self.false_part.variables
        return condition_variables | true_part_variables | false_part_variables

    def __eq__(self, other):
        if isinstance(other, Ternary):
            return self.__items == other.__items
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__items)

    def __iter__(self):
        return iter(self.__items)

    def __str__(self):
        return f"{self.condition}?{self.true_part}:{self.false_part}"


@typechecked
def parse_ternary(src: str) -> Tuple[Identifier, Interpolation, Interpolation]:
    """Parse an expression as a ternary.

    # Tests:
    >>> parse_ternary('reg7?them:him')
    (Identifier('reg7'), Interpolation('them'), Interpolation('him'))
    """
    if src.find("?") < 0:
        raise ValueError("Not an ternary: " + repr(src))
    split = src.split("?", maxsplit=1)
    if len(split) != 2:
        raise ValueError("Not an ternary: " + repr(src))
    condition, tail = split
    tail = split[1]
    depth = 0
    for pos, char in enumerate(tail):
        if char == ":":
            if depth == 0:
                break
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        if depth < 0:
            raise ValueError("Not an ternary: " + repr(src))
    else:
        raise ValueError("Not an ternary: " + repr(src))
    true_expr = tail[:pos]
    false_expr = tail[pos+1:]
    try:
        return Identifier(condition), Interpolation(true_expr), Interpolation(false_expr)
    except ValueError:
        raise ValueError("Not an ternary: " + repr(src))


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)


