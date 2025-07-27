from wa_typechecker import typechecked
from .Expression import Expression


class IdentifierExpression(Expression):
    """An identifier expression. See details in module description."""
    @typechecked
    def __init__(self, identifier: str):
        super().__init__((identifier,))

    @property
    def identifier(self) -> str:
        return self._items[0]

    def __str__(self):
        return f"{{{self.identifier}}}"
