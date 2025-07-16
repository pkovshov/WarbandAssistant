from collections.abc import Mapping
import logging
from typing import Dict, Iterator, Optional

from typeguard import typechecked

from .syntax.Errors import LangSyntaxError
from . import loader
from .syntax.Interpolation import Interpolation


class LangValue(Interpolation):
    """
    Tests:
    >>> print(repr(LangValue("{reg1?Herro:{reg2}}")))
    LangValue('{reg1?Herro:{reg2}}')
    >>> print(repr(LangValue("{reg1?Herro:{reg2", raw = True)))
    LangValue('{reg1?Herro:{reg2', raw = True)
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
    @typechecked()
    def __init__(self, data: dict[str, str]):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__data = {}
        for key, val in data.items():
            try:
                langval = LangValue(val)
            except LangSyntaxError as error:
                self.__logger.warning(f"Syntax error. Use raw mode with value: '{key}|{val}' Error: {error}")
                langval = LangValue(val, raw=True)
            self.__data[LangKey(key)] = langval

    def __getitem__(self, key: LangKey) -> LangValue:
        return self.__data[key]

    def __iter__(self) -> Iterator[LangKey]:
        return iter(self.__data)

    @typechecked
    def __contains__(self, key: LangKey) -> bool:
        return key in self.__data

    def __len__(self) -> int:
        return len(self.__data)


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
