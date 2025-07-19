import itertools
import logging
from typing import List, Optional

import mss
import numpy as np
from typeguard import typechecked

from wa_language import Language
from wa_language.model.types import PlayerSex
from .SampleMatch import SampleMatch
from .DialogScreen.DialogScreenManager import DialogScreenManager
from .MapScreen.MapScreenManager import MapScreenManager
from .GameUserFriendlyLogger import DialogScreenLogger
from .DatasetProcessors import MasterDatasetsProcessor


class GameScreenManager:
    @typechecked
    def __init__(self,
                 player_name: Optional[str],
                 player_sex: Optional[PlayerSex],
                 datasets: Optional[List[str]]):
        self.__logger = logging.getLogger(__name__)
        # TODO: someone need to warn if playername is blank string like '  '
        #       such name could broke fuzzy
        # TODO: warn if playername equal with other dialog titles (lorn names for example)
        #       or maybe is part of other dialog titles (Merchant for example)
        #       Also it needs to process such cases in DialogScreen
        # build language
        special_language = None
        if player_name is not None:
            special_language = {"wa_player": player_name}
        lang = Language.load(special_language)
        # create screen managers
        self.__map_screen_manger = MapScreenManager(lang)
        self.__dialog_screen_manger = DialogScreenManager(lang, player_sex)
        # create datasets processor that listens to screen manager
        if datasets:
            datasets_processor = MasterDatasetsProcessor(datasets=datasets,
                                                         player_name=player_name,
                                                         player_sex=player_sex)
            self.__map_screen_manger.add_event_listener(datasets_processor.on_map_screen)
            self.__dialog_screen_manger.add_event_listener(datasets_processor.on_dialog_screen)
        # create user-friendly logger that listens to screen managers
        self.__user_friendly_logger = DialogScreenLogger(lang)
        self.__map_screen_manger.add_event_listener(self.__user_friendly_logger.on_map_screen)
        self.__dialog_screen_manger.add_event_listener(self.__user_friendly_logger.on_dialog_screen)
        # log initial parameters
        self.__logger.info("Player: name {}, sex {}"
                           .format("NOT defined" if player_name is None else f"= {repr(player_name)}",
                                   "NOT defined" if player_sex is None else f"= {player_sex.value}"))

    @typechecked
    def run(self, monitor_idx: int):
        screen_managers = [self.__map_screen_manger,
                           self.__dialog_screen_manger]
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_idx]
            screen_managers_iter = itertools.cycle(screen_managers)
            current_screen_manager = next(screen_managers_iter)
            unknown_screen_manager = True
            user_friendly_messages = []

            def on_match_screen_manager():
                self.__logger.info(current_screen_manager.__class__.__name__)
                nonlocal unknown_screen_manager
                unknown_screen_manager = False

            def on_user_friendly_message(val):
                user_friendly_messages.append(val)

            self.__user_friendly_logger.listener = on_user_friendly_message
            self.__logger.info("Unknown")
            while True:
                scr = sct.grab(monitor)
                img = np.array(scr)[:, :, :3]  # BGRA -> BGR
                match = current_screen_manager.process(img)
                if match is SampleMatch.FAIL:
                    for screen_manager in screen_managers_iter:
                        if screen_manager is current_screen_manager:
                            if not unknown_screen_manager:
                                self.__logger.info("Unknown")
                                self.__user_friendly_logger.on_unknown_screen()
                                unknown_screen_manager = True
                            break  # we make a full loop
                        match = screen_manager.process(img)
                        if match is not SampleMatch.FAIL:
                            current_screen_manager = screen_manager
                            on_match_screen_manager()
                            break
                elif unknown_screen_manager:
                    on_match_screen_manager()
                while user_friendly_messages:
                    self.__logger.info(user_friendly_messages.pop(0))
