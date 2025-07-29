from wa_typechecker import typechecked
from .Expression import Expression


class BinaryExpression(Expression):
    """A binary expression. See details in module description."""
    @typechecked
    def __init__(self, left: str, right: str):
        super().__init__((left, right))

    @property
    def left(self) -> str:
        return self._items[0]  # type: ignore

    @property
    def right(self) -> str:
        return self._items[1]  # type: ignore

    def __str__(self):
        return f"{{{self.left}/{self.right}}}"
