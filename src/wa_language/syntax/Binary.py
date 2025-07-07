from typing import Tuple

from typeguard import typechecked

from .Expression import Expression

BINARY_CONDITION_VARIABLE = "wa_binary"
BINARY_CONDITION_VARIABLE_FIRST_VALUE = "first"
BINARY_CONDITION_VARIABLE_SECOND_VALUE = "second"

class Binary(Expression):
    """
    A Binary expression. See details in module description.

    Tests:
    >>> binar_1 = Binary('lord/lady')
    >>> print(binar_1.first)
    lord
    >>> print(binar_1.second)
    lady
    >>> print(binar_1)
    lord/lady
    >>> print(repr(binar_1))
    Binary('lord/lady')
    >>> binar_1 == eval(repr(binar_1))
    True
    >>> binar_2 = Binary('sir/madam')
    >>> binar_1 == binar_2
    False
    >>> hash(binar_1) == hash(binar_2)
    False
    >>> binar_3 = Binary('lord/lady')
    >>> binar_1 == binar_3
    True
    >>> hash(binar_1) == hash(binar_3)
    True
    >>> Binary("sir/madam/her")
    Traceback (most recent call last):
    ValueError: ...
    """
    @typechecked
    def __init__(self, src: str):
        super().__init__()
        self.__items = parse_binary(src)

    @property
    @typechecked
    def first(self) -> str:
        return self.__items[0]

    @property
    @typechecked
    def second(self) -> str:
        return self.__items[1]

    def _extract_variables(self):
        return frozenset((BINARY_CONDITION_VARIABLE,))

    def __eq__(self, other):
        if isinstance(other, Binary):
            return self.__items == other.__items
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__items)

    def __iter__(self):
        return iter(self.__items)

    def __str__(self):
        return f"{self.first}/{self.second}"


@typechecked
def parse_binary(src: str) -> Tuple[str, str]:
    """Parse an expression as a binary.

    Tests:
    >>> parse_binary("lord/lady")
    ('lord', 'lady')
    >>> parse_binary("q4 qIK _+?/")
    ('q4 qIK _+?', '')
    >>> parse_binary("/")
    ('', '')
    >>> parse_binary("Greeting.")
    Traceback (most recent call last):
    ValueError: ...
    >>> parse_binary("he/she/her")
    Traceback (most recent call last):
    ValueError: ...
    >>> parse_binary("{reg1}/ok")
    Traceback (most recent call last):
    ValueError: ...
    """
    if src.find("{") > 0 or src.find("}") > 0:
        raise ValueError("Not a binary: " + repr(src))
    if src.find("/") < 0:
        raise ValueError("Not a binary: " + repr(src))
    split = src.split("/")
    if len(split) != 2:
        raise ValueError("Not a binary: " + repr(src))
    return split[0], split[1]


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
