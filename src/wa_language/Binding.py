from collections.abc import Mapping
from typing import Any, Dict, Iterator, Union

from wa_typechecker import typechecked
from wa_language.LangVar import LangVar


class Binding(Mapping[LangVar, Any]):
    @typechecked
    def __init__(self, data: Dict[LangVar, Any]):
        # TODO: prevent copying for reliable sources
        self.__data = data.copy()

    def __getitem__(self, lang_var) -> Any:
        return self.__data[lang_var]

    def __iter__(self) -> Iterator[LangVar]:
        return iter(self.__data)

    def __contains__(self, lang_var) -> bool:
        return lang_var in self.__data

    def __len__(self) -> int:
        return len(self.__data)

    @typechecked
    def __or__(self, other: Union['Binding', Dict[LangVar, Any]]) -> 'Binding':
        if isinstance(other, Binding):
            merged = self.__data | other.__data
        elif isinstance(other, Dict):
            merged = self.__data | other
        else:
            return NotImplemented
        return Binding(merged)

    @typechecked
    def __ror__(self, other: Union['Binding', Dict[LangVar, Any]]) -> 'Binding':
        if isinstance(other, Binding):
            merged = other.__data | self.__data
        elif isinstance(other, Dict):
            merged = other | self.__data
        else:
            return NotImplemented
        return Binding(merged)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.__data)})"


EMPTY_BINDING = Binding(dict())
