import logging
from types import MappingProxyType
from typing import Mapping, Optional

import mss
import numpy as np
from typeguard import typechecked

from wa_language import LangLoader
from wa_language.LangValParser import Interpolation
from .DialogScreen.DialogScreenManager import DialogScreenManager
from .GameUserFriendlyLogger import DialogScreenLogger

class GameScreenManager:
    @typechecked
    def __init__(self, playername: Optional[str] = None, write_to_dataset: Optional[bool] = False):
        self.__logger = logging.getLogger(__name__)
        lang = self._load_lang(playername=playername)
        self.__dialog_screen_manger = DialogScreenManager(lang, write_to_dataset, playername)
        user_friendly_logger = DialogScreenLogger(lang)
        self.__dialog_screen_manger.add_event_listener(user_friendly_logger.process)
        if playername is None:
            self.__logger.info(f"playername NOT defined")
        else:
            self.__logger.info(f"playername = {repr(playername)}")

    @typechecked
    def run(self, monitor_idx: int):
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_idx]
            while True:
                scr = sct.grab(monitor)
                img = np.array(scr)[:, :, :3]  # BGRA -> BGR
                self.__dialog_screen_manger.process(img)

    @typechecked
    def _load_lang(self, playername: Optional[str]) -> Mapping[str, Interpolation]:
        lang = LangLoader.load_lang()
        # TODO: someone need to warn if playername is blank string like '  '
        #       such name could broke fuzzy
        # TODO: warn if playername equal with other dialog titles (lorn names for example)
        #       or maybe is part of other dialog titles (Merchant for example)
        #       Also it needs to process such cases in DialogScreen
        # TODO: extend load_files with a param accepting a dict with special keys
        # update lang with special keys
        if playername is not None:
            lang = lang | {"wa_player": Interpolation(playername, raw=True)}
        return MappingProxyType(lang)
