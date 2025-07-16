from typing import Any, Dict, Iterable

from typeguard import typechecked

from wa_language.syntax.Identifier import Identifier
from wa_language.syntax.Interpolation import Interpolation


class LangModelError(Exception):
    pass


class LangValueModel:
    @typechecked
    def __init__(self, model: Dict[Identifier, Iterable]):
        self.__model = {key: tuple(substitutions) for key, substitutions in model.items()}

    @typechecked
    def spread(self, lang_value: Interpolation, lang_var: Identifier) -> Dict[Any, Interpolation]:
        if lang_var not in self.__model:
            raise LangModelError("Spread with variable {repr(str(var))} absent in spread {self.__spread}")
        if lang_var not in lang_value.variables:
            raise LangModelError("Spread with variable {repr(str(var))} absent in lang value {repr(str(value))}")
        spread_dict = {substitution: lang_value.substitute(lang_var, str(substitution))
                       for substitution in self.__model[lang_var]}
        return spread_dict
