from collections import namedtuple
import logging
from typing import Mapping, Optional, Tuple

import rapidfuzz as fz
from typeguard import typechecked

from wa_language import LangValParser
from wa_language.model.troop_keys import is_troop_key


Result = namedtuple("Result", "score, keys")

TEXT = 0
SCORE = 1
KEY = 2


class DialogScreenFuzzy:
    @typechecked
    def __init__(self, lang: Mapping[str, LangValParser.Interpolation]):
        from . import dialog_screen_config
        self.__logger = logging.getLogger(__name__)
        self.__title_score_cutoff = dialog_screen_config.fuzzy_title_score_cutoff
        self.__logger.info(f"title_score_cutoff = {self.__title_score_cutoff}")
        self.__titles = {key: val for key, val in lang.items() if is_troop_key(key)}
        self.__prev_title_ocr = None
        self.__prev_title_keys = None

    @typechecked
    def title_key(self, title_ocr: str) -> Tuple[str, ...]:
        result = self.__cached_title(title_ocr)
        if result is None:
            return ()
        return result.keys

    @typechecked
    def title_score(self, title_ocr: str) -> Optional[float]:
        result = self.__cached_title(title_ocr)
        if result is None:
            return None
        return result.score

    def __cached_title(self, title_ocr: str) -> Optional[Result]:
        if title_ocr != self.__prev_title_ocr:
            self.__prev_title_ocr = title_ocr
            self.__prev_title_keys = self.__fuzzy_title(title_ocr)
        return self.__prev_title_keys

    def __fuzzy_title(self, title_ocr: str) -> Optional[Result]:
        choices = self.__titles
        # token set ratio with score cutoff
        matches = fz.process.extract(query=title_ocr,
                                     scorer=fz.fuzz.token_set_ratio,
                                     score_cutoff=self.__title_score_cutoff,
                                     choices=choices,
                                     limit=len(choices))
        if not matches:
            return None
        # build choices from matches
        choices = {key: choices[key] for _, _, key in matches}
        # sort matches by ratio
        matches = fz.process.extract(query=title_ocr,
                                     scorer=fz.fuzz.ratio,
                                     choices=choices,
                                     limit=len(choices))
        # filter best matches
        best_score = matches[0][SCORE]
        matches = [match for match in matches if match[SCORE] == best_score]
        # check that all best matches have the same text
        best_text = matches[0][TEXT]
        for match in matches:
            if match[TEXT] != best_text:
                self.__logger.warning(f"best matches have different texts: '{best_text}' and 'match[TEXT]'")
                break
        # build result
        keys = tuple(key for _, _, key in matches)
        return Result(best_score, keys)
