from collections import namedtuple
import logging
from typing import Mapping, Optional, Tuple

from wa_language import LangValParser
import numpy as np
from typeguard import typechecked

from . import DialogScreenModel


Cache = namedtuple("Cache",
                   "screen_sample_matches, "
                    # the most appropriate is using title_keys instead of title_ocr
                    # but I suppose that fuzzy provides same result for the same input
                   "title_ocr,"
                   "relation")


class DialogScreenLogger:
    @typechecked
    def __init__(self, lang: Mapping[str, LangValParser.Interpolation]):
        self.__logger = logging.getLogger(__name__)
        self.__lang = lang
        self.__cache = None

    @typechecked
    def process(self,
                image: np.ndarray,
                screen_sample_matches: bool,
                title_ocr: str,
                title: str,
                title_fuzzy_score: Optional[float],
                title_keys: Tuple[str, ...],
                relation_ocr: Optional[str],
                relation: Optional[int]):

        if self.__cache == Cache(screen_sample_matches, title_ocr, relation_ocr):
            return
        self.__cache = Cache(screen_sample_matches, title_ocr, relation_ocr)
        if not screen_sample_matches and not title_keys:
            return
        text = "Dialog: "
        if title_keys:
            title_key = title_keys[0]
            val = self.__lang[title_key]
            if DialogScreenModel.is_king(title_key):
                text += f"Ruler {val}"
            elif DialogScreenModel.is_lord(title_key):
                text += f"Lord {val}"
            elif DialogScreenModel.is_lady(title_key):
                text += f"Lady {val}"
            else:
                text += val
        else:
            text += title
        if relation_ocr is not None:
            text += f" {relation}" if relation is not None else "?"
        if screen_sample_matches and not title_keys:
            text += " (FALSE NEGATIVE)"
        if not screen_sample_matches:
            text += " (FALSE POSITIVE)"
        self.__logger.info(text)
