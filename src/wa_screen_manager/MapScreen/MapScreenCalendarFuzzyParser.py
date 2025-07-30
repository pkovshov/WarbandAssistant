from wa_typechecker import typechecked
from wa_language.LanguageModel import LanguageModel
from wa_model.calendar_model import YEAR_VAR, DAY_VAR
from .ModelFuzzyParser import ModelFuzzyParser
from .MapScreenEvent import DateTimeofday


class MapScreenCalendarFuzzyParser:
    @typechecked
    def __init__(self, date_model: LanguageModel, timeofday_model: LanguageModel):
        self.__date_model_parser = ModelFuzzyParser(date_model)
        self.__timeofday_model_parser = ModelFuzzyParser(timeofday_model)
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
        timeofday_bound = self.__timeofday_model_parser.bound(timeofday_ocr)
        if timeofday_bound is None:
            return None
        date_bound = self.__date_model_parser.bound(date_ocr)
        if date_bound is None:
            return None
        return DateTimeofday(date_key=date_bound.key,
                             year=date_bound.binding[YEAR_VAR],
                             day=date_bound.binding[DAY_VAR],
                             timeofday_key=timeofday_bound.key)
