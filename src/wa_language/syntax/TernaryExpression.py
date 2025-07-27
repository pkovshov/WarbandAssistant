from wa_typechecker import typechecked

from typing import Tuple

from .Expression import Expression
from .Identifier import Identifier
from .Interpolation import Interpolation
from .PlainText import PlainText


class TernaryExpression(Expression):
    @typechecked
    def __init__(self, items: Tuple[Identifier, Interpolation, Interpolation]):
        super().__init__(items)
        if self.true_part and isinstance(self.true_part[:-1], PlainText):
            if ":" not in self.true_part[:-1].blacklist:
                raise ValueError("true_part must not contain ':'")
        if self.false_part and isinstance(self.false_part[:-1], PlainText):
            if "}" not in self.false_part[:-1].blacklist:
                raise ValueError("false_part must not contain '}'")

    @property
    def condition(self) -> Identifier:
        return self._items[0]

    @property
    def true_part(self) -> Interpolation:
        return self._items[1]

    @property
    def false_part(self) -> Interpolation:
        return self._items[2]

    def __str__(self):
        return f"{{{self.condition}?{self.true_part}:{self.false_part}}}"
