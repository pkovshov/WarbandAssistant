import logging
from typing import Callable, Mapping, Optional

import numpy as np
from typeguard import typechecked

from wa_language import LangValParser
from wa_screen_manager.SampleMatch import SampleMatch
from .DialogScreenEvent import DialogScreenEvent
from .DialogScreenSamplers import DialogScreenScreenSampler, DialogScreenRelationSampler
from .DialogScreenOCRs import DialogScreenTitleOCR, DialogScreenRelationOCR
from .DialogScreenFuzzy import DialogScreenFuzzy
from .DialogScreenDatasetProcessor import DialogScreenDatasetProcessor


class DialogScreenManager:
    """DialogScreenManager class

    Responsible for:
    - processing Dialog Screens
    - manage samplers, ocrs and fuzzys
    - manage filling inferred dataset
    """
    @typechecked
    def __init__(self,
                 lang: Mapping[str, LangValParser.Interpolation],
                 write_to_dataset: bool = False,
                 playername: Optional[str] = None):
        self.__logger = logging.getLogger(__name__)
        self.__lang = lang
        self.__screen_sample = DialogScreenScreenSampler()
        self.__title_ocr = DialogScreenTitleOCR()
        self.__title_fuzzy = DialogScreenFuzzy(lang)
        self.__relation_sampler = DialogScreenRelationSampler()
        self.__relation_ocr = DialogScreenRelationOCR()
        self.__listeners = []
        if write_to_dataset:
            self.add_event_listener(DialogScreenDatasetProcessor(playername=playername).process)
        self.__prev__event = None

    @typechecked
    def add_event_listener(self, listener: Callable[[DialogScreenEvent], None]):
        if listener not in self.__listeners:
            self.__listeners.append(listener)

    @typechecked
    def process(self, img: np.ndarray) -> SampleMatch:
        screen_sample_matches = self.__screen_sample.check(img)
        if not screen_sample_matches:
            self.__prev__event = None
        else:
            title_ocr, title = self.__title_ocr.title(img)
            score = self.__title_fuzzy.title_score(title)
            keys = self.__title_fuzzy.title_key(title)
            relation_sampler_matches = self.__relation_sampler.check(img)
            if relation_sampler_matches:
                relation_ocr, relation = self.__relation_ocr.relation(img)
                assert relation_ocr is not None
            else:
                relation_ocr, relation = None, None
            event = DialogScreenEvent(image=img,
                                      title_ocr=title_ocr,
                                      title=title,
                                      title_fuzzy_score=score,
                                      title_keys=keys,
                                      relation_ocr=relation_ocr,
                                      relation=relation)
            if event != self.__prev__event:
                self.__prev__event = event
                for listener in self.__listeners:
                    listener(event)
        return screen_sample_matches
