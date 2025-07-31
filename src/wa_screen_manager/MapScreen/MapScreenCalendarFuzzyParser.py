import logging

from wa_typechecker import typechecked
from wa_language.LanguageModel import LanguageModel
from wa_model.calendar_model import YEAR_VAR, DAY_VAR
from ..BaseScreen.ModelFuzzyParser import ModelFuzzyParser
from .MapScreenEvent import DateTimeofday


class MapScreenCalendarFuzzyParser:
    @typechecked
    def __init__(self, date_model: LanguageModel, timeofday_model: LanguageModel):
        self.__date_model = date_model
        self.__timeofday_model = timeofday_model
        self.__model_fuzzy_parser = ModelFuzzyParser(score_cutoff=60)
        self.__prev_calendar_ocr = None
        self.__pref_date_timeofday = None

    @typechecked
    def calendar(self, calendar_ocr: str) -> DateTimeofday|None:
        if calendar_ocr != self.__prev_calendar_ocr:
            self.__prev_calendar_ocr = calendar_ocr
            self.__pref_date_timeofday = self.__fuzzy_calendar(calendar_ocr)
        return self.__pref_date_timeofday

    @typechecked
    def __fuzzy_calendar(self, calendar_ocr: str) -> DateTimeofday|None:
        split = calendar_ocr.split("\n")
        if len(split) != 2:
            return None
        date_ocr, timeofday_ocr = split
        timeofday_bounds = self.__model_fuzzy_parser.bounds(self.__timeofday_model,
                                                            timeofday_ocr).bounds
        if len(timeofday_bounds) == 0:
            return None
        date_bounds = self.__model_fuzzy_parser.bounds(self.__date_model,
                                                       date_ocr).bounds
        if len(date_bounds) == 0:
            return None
        if len(timeofday_bounds) > 1:
            logging.getLogger(__name__).warning(f"Several timeofdays are bound: {timeofday_bounds}")
        if len(date_bounds) > 1:
            logging.getLogger(__name__).warning(f"Several dates are bound: {date_bounds}")
        timeofday_bound = timeofday_bounds[0]
        date_bound = date_bounds[0]
        return DateTimeofday(date_key=date_bound.key,
                             year=date_bound.binding[YEAR_VAR],
                             day=date_bound.binding[DAY_VAR],
                             timeofday_key=timeofday_bound.key)
