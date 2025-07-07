import re

from typeguard import typechecked

from .Expression import Expression


class Identifier(Expression):
    """
    An identifier expression. See details in module description.

    Tests:
    >>> ident_1 = Identifier('s3')
    >>> print(ident_1.variable)
    s3
    >>> print(ident_1)
    s3
    >>> print(repr(ident_1))
    Identifier('s3')
    >>> ident_1 == eval(repr(ident_1))
    True
    >>> ident_2 = Identifier('reg5')
    >>> ident_1 == ident_2
    False
    >>> hash(ident_1) == hash(ident_2)
    False
    >>> ident_3 = Identifier('s3')
    >>> ident_1 == ident_3
    True
    >>> hash(ident_1) == hash(ident_3)
    True
    >>> Identifier("2")
    Traceback (most recent call last):
    ValueError: ...
    """
    @typechecked
    def __init__(self, src: str):
        super().__init__()
        self.__item = parse_identifier(src)

    @property
    @typechecked
    def variable(self) -> str:
        return self.__item

    def _extract_variables(self):
        return frozenset((self.variable,))

    def _substitute(self, variable: str, value: str):
        if variable == self.variable:
            return value
        else:
            return self

    def __eq__(self, other):
        if isinstance(other, Identifier):
            return self.__item == other.__item
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__item)

    def __str__(self):
        return self.__item


@typechecked
def parse_identifier(src: str) -> str:
    """Parse an expression as an identifier.
    Tests:
    >>> parse_identifier("s6")
    's6'
    >>> parse_identifier("reg14")
    'reg14'
    >>> parse_identifier("Ac97_342")
    'Ac97_342'
    >>> parse_identifier("__76wqe")
    '__76wqe'
    >>> parse_identifier("x")
    'x'
    >>> parse_identifier("_")
    '_'
    >>> parse_identifier("G")
    'G'
    >>> parse_identifier("5")
    Traceback (most recent call last):
    ValueError: ...
    >>> parse_identifier("86")
    Traceback (most recent call last):
    ValueError: ...
    >>> parse_identifier("s6:")
    Traceback (most recent call last):
    ValueError: ...
    >>> parse_identifier("s6?")
    Traceback (most recent call last):
    ValueError: ...
    """
    if re.fullmatch("([a-z]|[A-Z]|_)([a-z]|[A-Z]|_|[0-9])*", src):
        return src
    else:
        raise ValueError("Not an identifier: " + repr(src))


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)


