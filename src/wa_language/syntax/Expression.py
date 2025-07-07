from abc import ABC, abstractmethod
from typing import FrozenSet, Union

from typeguard import typechecked


class Expression(ABC):
    def __init__(self):
        self.__variables = None

    @property
    @typechecked
    def variables(self) -> FrozenSet[str]:
        if self.__variables is None:
            self.__variables = self._extract_variables()
        return self.__variables

    @abstractmethod
    def _extract_variables(self):
        raise NotImplemented

    @typechecked
    def substitute(self, variable: str, value: str) -> Union[str, "Expression"]:
        return self._substitute(variable, value)

    @abstractmethod
    def _substitute(self, variable: str, value: str):
        raise NotImplemented

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(str(self))})"
