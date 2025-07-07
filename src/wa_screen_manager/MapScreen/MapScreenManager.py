import logging
from typing import Callable, Mapping, Optional

import numpy as np
from typeguard import typechecked

from wa_language import LangValParser
from wa_screen_manager.BaseScreen.BaseSampler import BaseSampleReadingSampler
from wa_screen_manager.SampleMatch import SampleMatch
from .MapScreenEvent import MapScreenEvent
from .CalendarOCR import CalendarOCR


class MapScreenSampler(BaseSampleReadingSampler):
    def __init__(self):
        from .map_screen_config import map_screen_sample_img_path
        from wa_screen_manager.config import resolution
        from .map_screen_config import map_screen_sample_boxes
        super().__init__(sample_img_path=map_screen_sample_img_path,
                         resolution=resolution,
                         sample_boxes=map_screen_sample_boxes)


class MapScreenManager:
    """MapScreenManager class

    Responsible for:
    - processing Map Screens
    - manage sampler, ocr and fuzzy
    - manage filling inferred dataset
    """
    @typechecked
    def __init__(self,
                 lang: Mapping[str, LangValParser.Interpolation],
                 write_to_dataset: bool = False):
        self.__logger = logging.getLogger(__name__)
        self.__lang = lang
        self.__screen_sample = MapScreenSampler()
        self.__calendar_ocr = CalendarOCR()
        self.__listeners = []
        # if write_to_dataset:
        #     self.add_event_listener(DialogScreenDatasetProcessor(playername=playername).process)
        self.__prev__event = None

    @typechecked
    def add_event_listener(self, listener: Callable[[MapScreenEvent], None]):
        if listener not in self.__listeners:
            self.__listeners.append(listener)

    @typechecked
    def process(self, img: np.ndarray) -> SampleMatch:
        screen_sample_matches = self.__screen_sample.check(img)
        if not screen_sample_matches:
            self.__prev__event = None
        else:
            calendar_ocr = self.__calendar_ocr.ocr(img)
            event = MapScreenEvent(image=img,
                                   calendar_ocr=calendar_ocr)
            if event != self.__prev__event:
                self.__prev__event = event
                for listener in self.__listeners:
                    listener(event)
        return screen_sample_matches
