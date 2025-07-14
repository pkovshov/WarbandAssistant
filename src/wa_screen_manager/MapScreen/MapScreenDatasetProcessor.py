import logging
import subprocess
from typing import Optional, Tuple

import numpy as np
from typeguard import typechecked

from wa_datasets.MapScreen.MapCalendarDataset import MapCalendarDataset
from .MapScreenEvent import MapScreenEvent


class MapScreenDatasetProcessor:
    """Class that collects data for dialog screen datasets"""
    @typechecked
    def __init__(self):
        from . import map_screen_config
        from wa_screen_manager import config
        self.__logger = logging.getLogger(__name__)
        self.__map_calendar_dataset = MapCalendarDataset(resolution=config.resolution,
                                                         crop=map_screen_config.map_calendar_box,
                                                         language=config.language)

    @typechecked
    def process(self, event: MapScreenEvent):
        self.__map_calendar_dataset.add(screenshot=event.image,
                                        calendar_ocr=event.calendar_ocr,
                                        calendar_overlapped=event.calendar_overlapped,
                                        date_key=event.date_timeofday.date_key if event.date_timeofday is not None else None,
                                        year=event.date_timeofday.year if event.date_timeofday is not None else None,
                                        day=event.date_timeofday.day if event.date_timeofday is not None else None,
                                        timeofday_key=event.date_timeofday.timeofday_key if event.date_timeofday is not None else None,)
