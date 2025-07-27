"""Tests:
>>> parser = Identifier.parser()
>>> next(parser)
>>> try:
...    for s in "reg1":
...        parser.send(s)
...    next(parser)
... except StopIteration as result:
...    identifier = result.value
>>> expression = IdentifierExpression(identifier)
>>> print(expression)
{reg1}
"""

from typing import Tuple

from wa_typechecker import typechecked
from .Expression import Expression
from .Identifier import Identifier


class IdentifierExpression(Expression):
    """An identifier expression. See details in module description."""
    @typechecked
    def __init__(self, identifier: Identifier):
        super().__init__((identifier,))

    @property
    def identifier(self) -> Identifier:
        return self._items[0]

    def __str__(self):
        return f"{{{self.identifier}}}"
