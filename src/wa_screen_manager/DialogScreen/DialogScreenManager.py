import logging
from typing import Optional

import numpy as np
from wa_typechecker import typechecked

from wa_language.Language import Language
from wa_language.LangVar import PlayerSex
from ..SampleMatch import SampleMatch
from ..BaseScreen.GameScreenEventDispatcher import GameScreenEventDispatcher
from .DialogScreenEvent import DialogScreenEvent
from .DialogScreenSamplers import DialogScreenScreenSampler, DialogScreenRelationSampler
from .DialogScreenOCRs import DialogScreenTitleOCR, DialogScreenRelationOCR, DialogBodyOCR, NonStable
from .DialogScreenTitleFuzzyParser import DialogScreenTitleFuzzyParser
from .DialogScreenRelationParser import DialogScreenRelationParser
from .DialogBodyFuzzyParser import DialogBodyFuzzyParser


class DialogScreenManager(GameScreenEventDispatcher):
    """DialogScreenManager class

    Responsible for:
    - processing Dialog Screens
    - manage samplers, ocrs and fuzzys
    - manage filling inferred dataset
    """
    @typechecked
    def __init__(self,
                 lang: Language,
                 player_sex: Optional[PlayerSex] = None):
        super().__init__()
        self.__logger = logging.getLogger(__name__)
        self.__lang = lang
        self.__screen_sample = DialogScreenScreenSampler()
        self.__title_ocr = DialogScreenTitleOCR()
        self.__title_parser = DialogScreenTitleFuzzyParser(lang)
        self.__relation_sampler = DialogScreenRelationSampler()
        self.__relation_ocr = DialogScreenRelationOCR()
        self.__relation_parser = DialogScreenRelationParser()
        self.__body_ocr = DialogBodyOCR()
        self.__body_parser = DialogBodyFuzzyParser(lang, player_sex)
        self.__prev__event = None

    @typechecked
    def process(self, img: np.ndarray) -> SampleMatch:
        screen_sample_matches = self.__screen_sample.check(img)
        if not screen_sample_matches:
            self.__prev__event = None
        else:
            title_ocr = self.__title_ocr.ocr(img)
            if title_ocr is NonStable:
                self.__prev__event = None
            else:
                title_ocr_prep = self.__title_parser.prep(title_ocr)
                title_keys = self.__title_parser.keys(title_ocr_prep)
                relation_sampler_matches = self.__relation_sampler.check(img)
                relation_ocr, relation = None, None
                if relation_sampler_matches:
                    relation_ocr = self.__relation_ocr.ocr(img)
                    if relation_ocr is NonStable:
                        relation_ocr = None
                    else:
                        relation = self.__relation_parser.relation(relation_ocr)
                body_ocr = self.__body_ocr.ocr(img)
                if body_ocr is NonStable:
                    body_ocr = None
                if body_ocr is not None:
                    body_bounds = self.__body_parser.bound(body_ocr=body_ocr, title_keys=title_keys)
                else:
                    body_bounds = tuple()
                event = DialogScreenEvent(image=img,
                                          title_ocr=title_ocr,
                                          title_ocr_prep=title_ocr_prep,
                                          title_keys=title_keys,
                                          body_ocr=body_ocr,
                                          body_bounds=body_bounds,
                                          relation_ocr=relation_ocr,
                                          relation=relation)
                if event != self.__prev__event:
                    self.__prev__event = event
                    self._dispatch(event)
        return screen_sample_matches
