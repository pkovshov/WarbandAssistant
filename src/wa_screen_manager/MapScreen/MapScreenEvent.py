from typing import Optional, NamedTuple

import numpy as np
from wa_typechecker import typechecked

from wa_language.Language import LangKey
from wa_screen_manager.GameScreenEvent import GameScreenEvent


class DateTimeofday(NamedTuple):
    date_key: LangKey
    year: int
    day: int
    timeofday_key: LangKey


class MapScreenEvent(GameScreenEvent):
    @typechecked
    def __init__(self,
                 image: np.ndarray,
                 calendar_ocr: str,
                 calendar_overlapped: bool,
                 date_timeofday: Optional[DateTimeofday]):
        """
        :param image: An origin screenshot
        :param calendar_ocr: Result of calendar OCR.
        :param calendar_overlapped: Marks that calendar sampler does not match.
               That means a calendar is overlapped by caption of map object.
               For such case a date_timeofday value is not reliable.
               So, we need additional semantic analysis of date_timeofday value.
        :param date_timeofday: A fuzzy-parsed result of calendar OCR.
               Could be None if fuzzy-parcer does not provide any result with acceptable scores.
        """
        self.__image = image
        self.__calendar_ocr = calendar_ocr
        self.__calendar_overlapped = calendar_overlapped
        self.__date_timeofday = date_timeofday

    def __eq__(self, other):
        if not isinstance(other, MapScreenEvent):
            return NotImplemented
        # suppose that ocr provides same result for the same image
        # suppose that fuzzy parser provides same result for the same ocrs
        return (self.__calendar_ocr == other.__calendar_ocr and
                self.__calendar_overlapped == other.__calendar_overlapped)

    @property
    @typechecked
    def image(self) -> np.ndarray: return self.__image

    @property
    @typechecked
    def calendar_ocr(self) -> str: return self.__calendar_ocr

    @property
    @typechecked
    def calendar_overlapped(self) -> bool: return self.__calendar_overlapped

    @property
    @typechecked
    def date_timeofday(self) -> Optional[DateTimeofday]: return self.__date_timeofday
