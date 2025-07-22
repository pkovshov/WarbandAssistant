import itertools
import logging
from typing import Callable, List, Optional

import mss
import numpy as np
from typeguard import typechecked

from wa_language import Language
from wa_language.model.types import PlayerSex
from .SampleMatch import SampleMatch
from .DialogScreen.DialogScreenManager import DialogScreenManager
from .MapScreen.MapScreenManager import MapScreenManager
from .BaseScreen.GameScreenEventDispatcher import GameScreenEventDispatcher
from .GameUserFriendlyLogger import DialogScreenLogger
from .DatasetProcessors import MasterDatasetsProcessor
from .GameScreenEvent import UnknownScreenEvent


class GameScreenManager(GameScreenEventDispatcher):
    @typechecked
    def __init__(self,
                 player_name: Optional[str],
                 player_sex: Optional[PlayerSex],
                 datasets: Optional[List[str]]):
        super().__init__()
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
        # create screen managers, collect event dispatchers
        self.__map_screen_manager = MapScreenManager(lang)
        self.__dialog_screen_manger = DialogScreenManager(lang, player_sex)
        self.__game_screen_event_dispatchers = [
            self.__map_screen_manager,
            self.__dialog_screen_manger,
            self
        ]
        # create datasets processor and register it's game screen event handler
        if datasets:
            datasets_processor = MasterDatasetsProcessor(datasets=datasets,
                                                         player_name=player_name,
                                                         player_sex=player_sex)
            self.append_game_screen_event_handler(datasets_processor.on_game_screen_event)
        # create user-friendly logger and register it's game screen event handler
        user_friendly_logger = DialogScreenLogger(lang)
        self.append_game_screen_event_handler(user_friendly_logger.on_game_screen_event)
        # log initial parameters
        self.__logger.info("Player: name {}, sex {}"
                           .format("NOT defined" if player_name is None else f"= {repr(player_name)}",
                                   "NOT defined" if player_sex is None else f"= {player_sex.value}"))

    def append_game_screen_event_handler(self, handler):
        for dispatcher in self.__game_screen_event_dispatchers:
            dispatcher.append_handler(handler)

    @staticmethod
    def screen_manager_match(*screen_managers):
        screen_managers_cycle_iter = itertools.cycle(screen_managers)
        screenshot = yield None
        # infinite loop
        while screenshot is not None:
            # start processing from the last used screen manager
            # that is strictly needed if it matched the previous screenshot
            slice_start = len(screen_managers) - 1
            # end processing after trying all the screen managers
            slice_end = slice_start + len(screen_managers)
            # process screenshot
            for screen_manager in itertools.islice(screen_managers_cycle_iter,
                                                   slice_start,
                                                   slice_end):
                if screen_manager.process(screenshot) is not SampleMatch.FAIL:
                    screenshot = yield True
                    break
            else:
                screenshot = yield False

    @typechecked
    def run(self, monitor_idx: int):
        # prepare screen_manager_match generator and initialize got_match
        screen_manager_match = self.screen_manager_match(self.__map_screen_manager,
                                                         self.__dialog_screen_manger)
        next(screen_manager_match)
        got_match = True
        # got sct and use it as a context object
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_idx]
            while got_match is not None:
                # make screenshot
                screenshot = sct.grab(monitor)
                screenshot = np.array(screenshot)[:, :, :3]  # BGRA -> BGR
                # process screenshot
                match = screen_manager_match.send(screenshot)
                if got_match and not match:
                    self._dispatch(UnknownScreenEvent())
                got_match = match
