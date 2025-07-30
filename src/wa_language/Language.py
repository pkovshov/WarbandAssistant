from collections.abc import Mapping
from typing import Dict, Iterator, Optional

from wa_typechecker import typechecked

from . import loader
from .LangKey import LangKey
from .LangValue import LangValue


class Language(Mapping[LangKey, LangValue]):
    @typechecked
    def __init__(self, data: Dict[LangKey, LangValue]):
        self.__data = data

    def __getitem__(self, lang_key) -> LangValue:
        return self.__data[lang_key]

    def __iter__(self) -> Iterator[LangKey]:
        return iter(self.__data)

    def __contains__(self, lang_key) -> bool:
        return lang_key in self.__data

    def __len__(self) -> int:
        return len(self.__data)

    def __eq__(self, other) -> bool:
        # Comparison is an expensive operation.
        # Since Language is immutable, it's sufficient to check by instance identity.
        raise NotImplementedError("Use operator is instead of ==")


class RootLanguage(Language):
    @typechecked
    def __init__(self, data: Dict[str, str]):
        super().__init__({(lang_key := LangKey(key)): LangValue(val, self, lang_key)
                          for key, val in data.items()})


@typechecked
def load(special_language: Optional[Dict[str, str]] = None) -> Language:
    import path_conf
    lang_dir_path = path_conf.language
    lang_file_paths = loader.find_files(lang_dir_path)
    if len(lang_file_paths) == 0:
        raise ValueError(f"No csv files found at {lang_dir_path}")
    lang = loader.load_files(*lang_file_paths, special_language=special_language)
    if len(lang) == (len(special_language) if special_language else 0):
        raise ValueError(f"Empty lang is loaded by {lang_dir_path}")
    return RootLanguage(lang)


from . import LangValue as LangValueModule
LangValueModule.Language = Language
