from abc import ABC, abstractmethod
from typing import Hashable, Tuple

from wa_typechecker import typechecked


class Expression(ABC):
    @typechecked
    def __init__(self, items: Tuple[Hashable, ...]):
        self.__items = items

    @property
    def _items(self) -> Tuple[Hashable, ...]:
        return self.__items

    def __eq__(self, other):
        if isinstance(other, Expression):
            return self.__items == other.__items
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__items)

    @abstractmethod
    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ", ".join(repr(item) for item in self.__items))
