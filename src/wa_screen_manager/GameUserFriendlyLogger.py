from collections import namedtuple
import logging
from typing import Mapping, Optional, Tuple

from wa_language import LangValParser
import numpy as np
from typeguard import typechecked

from wa_language.model import troop_keys
from wa_screen_manager.DialogScreen.DialogScreenEvent import DialogScreenEvent
from wa_screen_manager.MapScreen.MapScreenEvent import MapScreenEvent


class DialogScreenLogger:
    @typechecked
    def __init__(self, lang: Mapping[str, LangValParser.Interpolation]):
        self.__logger = logging.getLogger(__name__)
        self.__lang = lang
        self.__cache = None

    @typechecked
    def on_map_screen(self, event: MapScreenEvent):
        self.__logger.info("calendar_ocr: " + repr(event.calendar_ocr))

    @typechecked
    def on_dialog_screen(self, event: DialogScreenEvent):
        text = "Dialog: "
        if event.title_keys:
            title_key = event.title_keys[0]
            val = self.__lang[title_key]
            if troop_keys.is_king_key(title_key):
                text += f"Ruler {val}"
            elif troop_keys.is_lord_key(title_key):
                text += f"Lord {val}"
            elif troop_keys.is_lady_key(title_key):
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
