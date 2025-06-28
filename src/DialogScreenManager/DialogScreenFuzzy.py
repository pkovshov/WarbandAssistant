import logging
from typing import Mapping, Optional

from mbw_language import LangValParser
import rapidfuzz as fz
from typeguard import typechecked

from .DialogScreenModel import is_dialog_title_key

class DialogScreenFuzzy:
    @typechecked
    def __init__(self, lang: Mapping[str, LangValParser.Interpolation]):
        from . import dialog_screen_config
        self.__logger = logging.getLogger(__name__)
        self.__title_score_cutoff = dialog_screen_config.fuzzy_title_score_cutoff
        self.__logger.info(f"title_score_cutoff = {self.__title_score_cutoff}")
        self.__titles = {key: val for key, val in lang.items() if is_dialog_title_key(key)}

    @typechecked
    def title_key(self, title: str) -> Optional[str]:
        best_match = fz.process.extractOne(query=title,
                                           choices=self.__titles,
                                           scorer=fz.fuzz.token_set_ratio,
                                           score_cutoff=self.__title_score_cutoff)
        if best_match is None:
            return None
        _, _, key = best_match
        val = self.__titles[key]
        return key
