import logging
from typing import Callable, Mapping, Optional

import numpy as np
from typeguard import typechecked

from wa_language.Language import Language
from wa_screen_manager.BaseScreen.BaseSampler import BaseSampleReadingSampler
from wa_screen_manager.SampleMatch import SampleMatch
from ..BaseScreen.GameScreenEventDispatcher import GameScreenEventDispatcher
from .MapScreenEvent import MapScreenEvent, GameScreenEvent
from .MapScreenCalendarOCR import MapScreenCalendarOCR, NonStable
from .MapScreenCalendarFuzzyParser import MapScreenCalendarFuzzyParser


# TODO: use BaseSampler to prevent reading map_screen_blank_img_path twice


class MapScreenSampler(BaseSampleReadingSampler):
    def __init__(self):
        from .map_screen_config import map_screen_blank_img_path
        from wa_screen_manager.config import resolution
        from .map_screen_config import map_screen_sample_boxes
        super().__init__(sample_img_path=map_screen_blank_img_path,
                         resolution=resolution,
                         sample_boxes=map_screen_sample_boxes)


class MapCalendarSampler(BaseSampleReadingSampler):
    def __init__(self):
        from .map_screen_config import map_screen_blank_img_path
        from wa_screen_manager.config import resolution
        from .map_screen_config import map_calendar_sample_boxes
        super().__init__(sample_img_path=map_screen_blank_img_path,
                         resolution=resolution,
                         sample_boxes=map_calendar_sample_boxes)


class MapScreenManager(GameScreenEventDispatcher):
    """MapScreenManager class

    Responsible for:
    - processing Map Screens
    - manage sampler, ocr and fuzzy
    - manage filling inferred dataset
    """
    @typechecked
    def __init__(self,
                 lang: Language):
        super().__init__()
        self.__logger = logging.getLogger(__name__)
        self.__lang = lang
        self.__screen_sample = MapScreenSampler()
        self.__calendar_sample = MapCalendarSampler()
        self.__calendar_ocr = MapScreenCalendarOCR()
        self.__calendar_fuzzy_parser = MapScreenCalendarFuzzyParser(lang)
        self.__prev__event = None

    @typechecked
    def process(self, img: np.ndarray) -> SampleMatch:
        screen_sample_matches = self.__screen_sample.check(img)
        if not screen_sample_matches:
            self.__prev__event = None
        else:
            calendar_ocr = self.__calendar_ocr.ocr(img)
            if calendar_ocr is NonStable:
                pass
            else:
                calendar_sample_matches = self.__calendar_sample.check(img)
                date_timeofday = self.__calendar_fuzzy_parser.calendar(calendar_ocr)
                event = MapScreenEvent(image=img,
                                       calendar_ocr=calendar_ocr,
                                       calendar_overlapped=not calendar_sample_matches,
                                       date_timeofday=date_timeofday)
                if event != self.__prev__event:
                    self.__prev__event = event
                    self._dispatch(event)
        return screen_sample_matches
