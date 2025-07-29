from collections.abc import Mapping
from enum import Enum
from typing import Any, Dict, Iterator, Union

from wa_typechecker import typechecked
from .LangVar import LangVar


class PlayerSex(Enum):
    MALE = 'male'
    FEMALE = 'female'


class Binding(Mapping[LangVar, Any]):
    @typechecked
    def __init__(self, data: Dict[LangVar, Any]):
        self.__data = data.copy()

    @typechecked
    def __getitem__(self, key: LangVar) -> Any:
        return self.__data[key]

    def __iter__(self) -> Iterator[LangVar]:
        return iter(self.__data)

    @typechecked
    def __contains__(self, key: LangVar) -> bool:
        return key in self.__data

    def __len__(self) -> int:
        return len(self.__data)

    def __or__(self, other: Union['Binding', Dict]) -> 'Binding':
        if isinstance(other, Binding):
            merged = self.__data | other.__data
        elif isinstance(other, Dict):
            merged = self.__data | other
        else:
            return NotImplemented
        return Binding(merged)

    def __ror__(self, other: Union['Binding', Dict]) -> 'Binding':
        if isinstance(other, Binding):
            merged = other.__data | self.__data
        elif isinstance(other, Dict):
            merged = other | self.__data
        else:
            return NotImplemented
        return Binding(merged)


EMPTY_BINDING = Binding(dict())
