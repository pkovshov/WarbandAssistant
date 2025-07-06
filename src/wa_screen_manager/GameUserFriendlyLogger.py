from collections import namedtuple
import logging
from typing import Mapping, Optional, Tuple

from wa_language import LangValParser
import numpy as np
from typeguard import typechecked

from wa_screen_manager.DialogScreen import DialogScreenModel
from wa_screen_manager.DialogScreen.DialogScreenEvent import DialogScreenEvent

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
    def process(self, event: DialogScreenEvent):
        text = "Dialog: "
        if event.title_keys:
            title_key = event.title_keys[0]
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
            text += repr(event.title)
        if event.relation_ocr is not None:
            text += " "
            text += str(event.relation) if event.relation is not None else "?"
        if not event.title_keys:
            text += " (FALSE NEGATIVE)"
        self.__logger.info(text)
