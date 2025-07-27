from wa_typechecker import typechecked
from .Expression import Expression
from .Interpolation import Interpolation


class TernaryExpression(Expression):
    """A ternary expression. See details in module description."""
    @typechecked
    def __init__(self, condition: str, true_part: Interpolation, false_part: Interpolation):
        super().__init__((condition, true_part, false_part))

    @property
    def condition(self) -> str:
        return self._items[0]

    @property
    def true_part(self) -> Interpolation:
        return self._items[1]

    @property
    def false_part(self) -> Interpolation:
        return self._items[2]

    def __str__(self):
        return f"{{{self.condition}?{self.true_part}:{self.false_part}}}"
