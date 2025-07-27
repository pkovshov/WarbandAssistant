from typing import Any, Dict, Iterable

from wa_typechecker import typechecked

from wa_language.Language import (BINARY_CONDITION_VARIABLE,
                                  BINARY_CONDITION_VARIABLE_FIRST_VALUE,
                                  BINARY_CONDITION_VARIABLE_SECOND_VALUE)

from wa_language.syntax.Interpolation import Interpolation


class LangModelError(Exception):
    pass


class LangValueModel:
    @typechecked
    def __init__(self, model: Dict[str, Iterable]):
        self.__model = {key: tuple(substitutions) for key, substitutions in model.items()}

    @typechecked
    def spread(self, lang_value: Interpolation, lang_var: str) -> Dict[Any, Interpolation]:
        if lang_var not in self.__model:
            raise LangModelError("Spread with variable {repr(str(var))} absent in spread {self.__spread}")
        # if lang_var not in lang_value.variables:
        #     raise LangModelError("Spread with variable {repr(str(var))} absent in lang value {repr(str(value))}")
        spread_dict = {substitution: lang_value.substitute(lang_var, str(substitution))
                       for substitution in self.__model[lang_var]}
        return spread_dict

class SexLangValueModel(LangValueModel):
    def __init__(self):
        super().__init__({BINARY_CONDITION_VARIABLE: (BINARY_CONDITION_VARIABLE_FIRST_VALUE,
                                                      BINARY_CONDITION_VARIABLE_SECOND_VALUE)})

    @typechecked
    def spread(self, lang_value: Interpolation) -> Dict[Any, Interpolation]:
        return super().spread(lang_value, BINARY_CONDITION_VARIABLE)
