from collections.abc import Mapping
import logging
from typing import Dict, Iterator, Optional

from wa_typechecker import typechecked

from . import loader
from .syntax.Interpolation import Interpolation
from .syntax.Identifier import Identifier


BINARY_CONDITION_VARIABLE = Identifier("wa_binary")
BINARY_CONDITION_VARIABLE_FIRST_VALUE = "first"
BINARY_CONDITION_VARIABLE_SECOND_VALUE = "second"

class LangValue(Interpolation):
    """
    Tests:
    >>> print(str(LangValue("{reg1?Herro:{reg2}}")))
    {reg1?Herro:{reg2}}
    >>> print(str(LangValue("{reg1?Herro:{reg2")))
    {reg1?Herro:{reg2
    """
    pass


class LangKey(str):
    """
    Tests:
    >>> print(repr(LangKey("wa_player")))
    LangKey('wa_player')
    """
    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, repr(str(self)))



class Language(Mapping[LangKey, LangValue]):
    @typechecked
    def __init__(self, data: dict[str, str]):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__data = {}
        for key, val in data.items():
            langval = LangValue(val)
            self.__data[LangKey(key)] = langval

    @typechecked
    def __getitem__(self, key: LangKey) -> LangValue:
        return self.__data[key]

    def __iter__(self) -> Iterator[LangKey]:
        return iter(self.__data)

    @typechecked
    def __contains__(self, key: LangKey) -> bool:
        return key in self.__data

    def __len__(self) -> int:
        return len(self.__data)

    def __eq__(self, other) -> bool:
        # Comparison is an expensive operation.
        # Since Language is immutable, it's sufficient to check by instance identity.
        raise NotImplemented("Use operator is instead of ==")


class LangContentError(Exception):
    pass


@typechecked
def load(special_language: Optional[Dict[str, str]] = None) -> Language:
    import path_conf
    lang_dir_path = path_conf.language
    lang_file_paths = loader.find_files(lang_dir_path)
    if len(lang_file_paths) == 0:
        raise LangContentError(f"No csv files found at {lang_dir_path}")
    lang = loader.load_files(*lang_file_paths, special_language=special_language)
    if len(lang) == (len(special_language) if special_language else 0):
        raise LangContentError(f"Empty lang is loaded by {lang_dir_path}")
    return Language(lang)
