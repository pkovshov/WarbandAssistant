from typing import Any, Dict, Iterable

from wa_typechecker import typechecked

from wa_language.LangValue import LangValue
from wa_language.LangVar import LangVar, PlayerSex
from wa_language.LangVar import PlayerSexVar
from wa_language.Spreading import SpreadType


class LangModelError(Exception):
    pass


class LangValueModel:
    @typechecked
    def __init__(self, model: Dict[str, SpreadType]):
        self.__model = model.copy()

    @typechecked
    def spread(self, lang_value: LangValue, lang_var: LangVar) -> Dict[Any, LangValue]:
        if lang_var not in self.__model:
            raise LangModelError("Spread with variable {repr(str(var))} absent in spread {self.__spread}")
        # if lang_var not in lang_value.variables:
        #     raise LangModelError("Spread with variable {repr(str(var))} absent in lang value {repr(str(value))}")
        spread_dict = {substitution: lang_value.bind(lang_var, substitution)
                       for substitution in self.__model[lang_var]}
        return spread_dict


class SexLangValueModel(LangValueModel):
    def __init__(self):
        super().__init__({PlayerSexVar: (PlayerSex.MALE,
                                         PlayerSex.FEMALE)})

    @typechecked
    def spread(self, lang_value: LangValue) -> Dict[Any, LangValue]:
        return super().spread(lang_value, PlayerSexVar)
