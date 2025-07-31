from collections.abc import Collection, Mapping
from typing import get_args, overload, Dict, Iterator, Union

from wa_typechecker import typechecked
from .LangVar import LangVar


SpreadType = Union[tuple, range]


class Spread(Collection):
    @overload
    def __init__(self, items: SpreadType):
        ...

    @overload
    def __init__(self, *args):
        ...

    @typechecked
    def __init__(self, *args):
        if len(args) == 1:
            items = args[0]
        else:
            items = args
        if not isinstance(items, get_args(SpreadType)):
            raise TypeError(f"insufficient argument type: expected {get_args(SpreadType)}, got {items}")
        if len(items) == 0:
            raise ValueError(f"empty items {items}")
        # we don't need to copy due to all the SpreadType cases are immutable
        self.__items = items

    def __contains__(self, item) -> bool:
        return item in self.__items

    def __iter__(self) -> Iterator:
        return iter(self.__items)

    def __len__(self) -> int:
        return len(self.__items)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.__items)})"


class Spreading(Mapping[LangVar, Spread]):
    @typechecked
    def __init__(self, data: dict[LangVar, Spread]):
        # TODO: prevent copying for reliable sources
        self.__data = data.copy()

    def __getitem__(self, lang_var) -> Spread:
        return self.__data[lang_var]

    def __iter__(self) -> Iterator[LangVar]:
        return iter(self.__data)

    def __contains__(self, lang_var) -> bool:
        return lang_var in self.__data

    def __len__(self) -> int:
        return len(self.__data)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.__data)})"


EMPTY_SPREADING = Spreading(dict())
