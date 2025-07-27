"""
Tests:
>>> parser = BinaryExpression.parser(prefix=["{"])
>>> next(parser)
>>> try:
...    for s in "man/woman}":
...        parser.send(s)
... except StopIteration as stop:
...    binary = stop.value
>>> isinstance(binary, BinaryExpression)
True
>>> print(binary)
{man/woman}
>>> parser = BinaryExpression.parser(prefix=["{"])
>>> next(parser)
>>> try:
...    for s in "manwoman}":
...        parser.send(s)
... except StopIteration as stop:
...    binary = stop.value
>>> isinstance(binary, BinaryExpression)
False
>>> print(binary)
{manwoman
"""

from typing import Any, Collection, Tuple

from wa_typechecker import typechecked
from .Expression import Expression
from .Identifier import Identifier
from .PlainText import PlainText


class BinaryExpression(Expression):
    """A binary expression. See details in module description."""
    def __new__(self, items: Tuple[PlainText, PlainText]):
        raise NotImplementedError("use parser generator")

    @typechecked
    def __init__(self, items: Tuple[str, str]):
        super().__init__(items)

    @property
    def left(self) -> PlainText:
        return self._items[0]

    @property
    def right(self) -> PlainText:
        return self._items[1]

    def __str__(self):
        return f"{{{self.left}/{self.right}}}"

    @classmethod
    def parser(cls, prefix: Collection[Any]):
        """Generator

        Accepts one symbol in a row to be sent.
        Ends when a return statement raises StopIteration.
        The StopIteration value is either BinaryExpression
        or a str instance if iteration syntax was violated.
        """
        assert 1 <= len(prefix) <= 2
        first_symbol = prefix[0]
        assert first_symbol == "{"
        if len(prefix) == 2:
            left = prefix[1]
            assert isinstance(left, Identifier)
            left = list(str(left))
        else:
            left = []
        # parse left
        symbol = yield
        while symbol is not None and symbol not in "}/":
            left.append(symbol)
            symbol = yield
        if symbol is None or symbol == "}":
            return f"{first_symbol}{''.join(left)}"
        # parse right
        right = []
        symbol = yield
        while symbol is not None and symbol != "}":
            right.append(symbol)
            symbol = yield
        if symbol is None:
            return f"{first_symbol}{''.join(left)}{''.join(right)}"
        inst = super().__new__(cls)
        inst.__init__((''.join(left), ''.join(right)))
        return inst
