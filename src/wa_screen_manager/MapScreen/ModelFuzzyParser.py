import rapidfuzz as fz

from wa_typechecker import typechecked
from wa_language.LangValue import LangValue
from wa_language.LanguageModel import LanguageModel


VALUE = 0
SCORE = 1
KEY = 2


class ModelFuzzyParser:
    @typechecked
    def __init__(self, model: LanguageModel):
        self.__model = model
        self.__prev_ocr: str | None = None
        self.__prev_bounds: LangValue | None = None

    @typechecked
    def bound(self, ocr: str) -> LangValue | None:
        if ocr != self.__prev_ocr:
            self.__prev_ocr = ocr
            self.__prev_bounds = self.__bound(ocr)
        return self.__prev_bounds

    def __bound(self, ocr: str) -> LangValue|None:
        score_cutoff = 60
        choices = self.__model.purge_spread
        match = fz.process.extractOne(query=ocr,
                                      scorer=fz.fuzz.ratio,
                                      choices=choices)
        value: LangValue = match[VALUE]
        spreading = self.__model[value.key]
        value = self.__model.language[value.key]
        for var, spread in spreading.items():
            choices = value.spread(var, spread)
            match = fz.process.extractOne(query=ocr,
                                          scorer=fz.fuzz.ratio,
                                          choices=choices)
            value: LangValue = match[VALUE]
        if match[SCORE] >= score_cutoff:
            return value
        else:
            return None
