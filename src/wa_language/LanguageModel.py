from collections.abc import Mapping
import itertools
from typing import Dict, Iterator, Optional

from wa_typechecker import typechecked
from .Binding import Binding
from .KeyChecker import KeyChecker
from .LangKey import LangKey
from .LangValue import LangValue
from .LangVar import PlayerSex, PlayerSexVar, PLAYER_NAME_VAR
from .Language import Language
from .Spreading import Spreading, Spread


class LanguageModel(Mapping[LangKey, Spreading]):
    def __init__(self,
                 model: Dict[KeyChecker, Spreading],
                 language: Language,
                 symbols: str = None,
                 player_name: Optional[str] = None,
                 player_sex: Optional[PlayerSex] = None):
        # TODO: remove __root_language
        self.__root_language = language
        # build keychecker_languages for extracting LangKeys and LangValues
        # TODO: checks that keychecker_languages do not intersect and override each other
        #       log warning for such case
        keychecker_languages = {keychecker: keychecker.lang(language)
                                for keychecker in model}
        # build inner model that provides a Spreading for each model LangKey
        self.__model: Dict[LangKey, Spreading] = {}
        for keychecker, lang in keychecker_languages.items():
            spreading = model[keychecker]
            for key in lang:
                self.__model[key] = spreading
        # build model language, that bind language values with player's name and sex
        self.__language = {}
        # # construct player_name_sex binding
        player_name_sex_binding = {}
        if player_name is not None:
            player_name_sex_binding[PLAYER_NAME_VAR] = player_name
        if player_sex is not None:
            player_name_sex_binding[PlayerSexVar] = player_sex
        player_name_sex_binding = Binding(player_name_sex_binding)
        # # apply player_name_sex binding
        for lang in keychecker_languages.values():
            for key, val in lang.items():
                self.__language[key] = val.bind(player_name_sex_binding)
        self.__language = Language(self.__language)
        # build model purge spread from all the model lang values' purge spreads
        purge_spread = itertools.chain.from_iterable(
            val.purge_spread() for val in self.__language.values())
        if player_sex is None:
            # construct and apply player_sex spreading
            player_sex_spreading = Spreading({PlayerSexVar: Spread(PlayerSex.MALE, PlayerSex.FEMALE)})
            purge_spread = itertools.chain.from_iterable(
                val.spread(player_sex_spreading) for val in purge_spread)
        self.__purge_spread = tuple(purge_spread)
        # build symbols considering purge spread and all the model spreadings
        if symbols is not None:
            self.__symbols = symbols
        else:
            symbols = set()
            # consider purge spread
            for val in self.__purge_spread:
                symbols |= set(val)
            # consider sreadings
            for keychecker, lang in keychecker_languages.items():
                # apply spreading values only if keychecker found keys within root language
                if len(lang) > 0:
                    for spread in model[keychecker].values():
                        for spread_item in spread:
                            symbols |= set(str(spread_item))
            self.__symbols = "".join(symbols)

    @property
    def language(self) -> Language:
        return self.__language

    @property
    def purge_spread(self) -> tuple[LangValue]:
        return self.__purge_spread

    @property
    def symbols(self) -> str:
        return self.__symbols

    def __getitem__(self, lang_key) -> Spreading:
        return self.__model[lang_key]

    def __iter__(self) -> Iterator[LangKey]:
        return iter(self.__model)

    def __contains__(self, lang_key) -> bool:
        return lang_key in self.__model

    def __len__(self) -> int:
        return len(self.__model)
