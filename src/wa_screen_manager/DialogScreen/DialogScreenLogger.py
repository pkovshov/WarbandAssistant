import logging
from typing import Mapping, Optional, Tuple

from wa_language import LangValParser
import numpy as np
from typeguard import typechecked

from . import DialogScreenModel


class DialogScreenLogger:
    @typechecked
    def __init__(self, lang: Mapping[str, LangValParser.Interpolation]):
        self.__logger = logging.getLogger(__name__)
        self.__lang = lang
        self.__cache = None

    @typechecked
    def process(self,
                image: np.ndarray,
                dialog_sample_matches: bool,
                title_ocr: str,
                title_fuzzy_score: Optional[float],
                title_keys: Tuple[str, ...]):
        # the most appropriate cache is (sample_matches, title_keys)
        # but I suppose that fuzzy provides same result for the same input
        if self.__cache == (dialog_sample_matches, title_ocr):
            return
        self.__cache = dialog_sample_matches, title_ocr
        text = None
        if title_keys:
            text = "Dialog: "
            title_key = title_keys[0]
            val = self.__lang[title_key]
            if DialogScreenModel.is_king(title_key):
                text += repr(f"Ruler {val}")
            elif DialogScreenModel.is_lord(title_key):
                text += repr(f"Lord {val}")
            elif DialogScreenModel.is_lady(title_key):
                text += repr(f"Lady {val}")
            else:
                text = val
            if not dialog_sample_matches:
                text += " (FALSE POSITIVE)"
        elif dialog_sample_matches:
            text = repr("") + " (FALSE NEGATIVE)"
        if text is not None:
            self.__logger.info(text)
