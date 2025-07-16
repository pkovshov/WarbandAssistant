import logging
from typing import Mapping, Optional

import rapidfuzz as fz
from typeguard import typechecked

from wa_language.Language import Language
from wa_language.model.calendar_model import is_date_key, is_timeofday_key, DateValueModel
from .MapScreenEvent import DateTimeofday

TEXT = 0
SCORE = 1
KEY = 2

class MapScreenCalendarFuzzyParser:
    @typechecked
    def __init__(self, lang: Language):
        self.__logger = logging.getLogger(__name__)
        self.__timeofday_lang = is_timeofday_key(lang)
        self.__date_lang = is_date_key(lang)
        self.__date_model = DateValueModel()
        self.__month_spread = {key: val.substitute(DateValueModel.YEAR_VAR, "")
                                       .substitute(DateValueModel.DAY_VAR, "")
                               for key, val in self.__date_lang.items()}
        self.__prev_calendar_ocr = None
        self.__pref_date_timeofday = None

    @typechecked
    def calendar(self, calendar_ocr: str) -> Optional[DateTimeofday]:
        if calendar_ocr != self.__prev_calendar_ocr:
            self.__prev_calendar_ocr = calendar_ocr
            self.__pref_date_timeofday = self.__fuzzy_calendar(calendar_ocr)
        return self.__pref_date_timeofday

    @typechecked
    def __fuzzy_calendar(self, calendar_ocr: str) -> Optional[DateTimeofday]:
        split = calendar_ocr.split("\n")
        if len(split) != 2:
            return None
        score_cutoff = 60
        date_ocr, timeofday_ocr = split
        # find the best timeofday key
        # apply score cutoff
        timeofday_match = fz.process.extractOne(query=timeofday_ocr,
                                                scorer=fz.fuzz.ratio,
                                                choices=self.__timeofday_lang,
                                                score_cutoff=score_cutoff)
        # check on None due to cutoff
        if timeofday_match is None:
            return None
        timeofday_key = timeofday_match[KEY]
        # find the best date key
        date_match = fz.process.extractOne(query=date_ocr,
                                           scorer=fz.fuzz.ratio,
                                           choices=self.__month_spread)
        date_key = date_match[KEY]
        # build year spread
        year_spread = self.__date_model.spread(self.__date_lang[date_key],
                                               DateValueModel.YEAR_VAR)
        # find the best year for found date key
        date_match = fz.process.extractOne(query=date_ocr,
                                           scorer=fz.fuzz.ratio,
                                           choices=year_spread)
        year = date_match[KEY]
        # build day spread
        day_spread = self.__date_model.spread(date_match[TEXT],
                                              DateValueModel.DAY_VAR)
        # find the best day for found date key and year
        # apply score cutoff
        date_match = fz.process.extractOne(query=date_ocr,
                                           scorer=fz.fuzz.ratio,
                                           choices=day_spread,
                                           score_cutoff=score_cutoff)
        # check on None due to cutoff
        if date_match is None:
            return None
        day = date_match[KEY]
        return DateTimeofday(date_key=date_key,
                             year=year,
                             day=day,
                             timeofday_key=timeofday_key)
