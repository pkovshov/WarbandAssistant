import logging
from typing import Mapping

import numpy as np
from typeguard import typechecked
from typing import Optional

from wa_types import is_screenshot
from wa_language import LangValParser
from .DialogScreenSamplers import DialogScreenScreenSampler, DialogScreenRelationSampler
from .DialogScreenOCRs import DialogScreenTitleOCR, DialogScreenRelationOCR
from .DialogScreenFuzzy import DialogScreenFuzzy
from .DialogScreenDatasetProcessor import DialogScreenDatasetProcessor
from .DialogScreenLogger import DialogScreenLogger


class DialogScreenManager:
    """DialogScreenManager class

    Responsible for:
    - processing Game Screens
    - manage sample, ocr and fuzzy
    - manage filling inferred dataset
    """
    @typechecked
    def __init__(self,
                 lang: Mapping[str, LangValParser.Interpolation],
                 write_to_dataset: bool = False,
                 playername: Optional[str] = None,
                 force_parsing: bool = False):
        self.__logger = logging.getLogger(__name__)
        self.__lang = lang
        self.__screen_sample = DialogScreenScreenSampler()
        self.__title_ocr = DialogScreenTitleOCR()
        self.__title_fuzzy = DialogScreenFuzzy(lang)
        self.__relation_sampler = DialogScreenRelationSampler()
        self.__relation_ocr = DialogScreenRelationOCR()
        self.__force_parsing = force_parsing
        self.__artifacts_processors = []
        if write_to_dataset:
            self.__artifacts_processors.append(
                DialogScreenDatasetProcessor(playername=playername).process)
        self.__artifacts_processors.append(
            DialogScreenLogger(self.__lang).process)
        self.__prev__title_ocr = None

    def process(self, img: np.ndarray):
        screen_sample_matches = self.__screen_sample.check(img)
        if screen_sample_matches or self.__force_parsing:
            title_ocr, title = self.__title_ocr.title(img)
            score = self.__title_fuzzy.title_score(title)
            keys = self.__title_fuzzy.title_key(title)
            relation_sampler_matches = self.__relation_sampler.check(img)
            if relation_sampler_matches:
                relation_ocr, relation = self.__relation_ocr.relation(img)
                assert relation_ocr is not None
            else:
                relation_ocr, relation = None, None
            # process artifacts
            for processor in self.__artifacts_processors:
                processor(image=img,
                          screen_sample_matches=screen_sample_matches,
                          title_ocr=title_ocr,
                          title=title,
                          title_fuzzy_score=score,
                          title_keys=keys,
                          relation_ocr=relation_ocr,
                          relation=relation)
