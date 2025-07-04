import logging
from typing import Mapping

from wa_language import LangValParser
import numpy as np
from typeguard import typechecked
from typing import Optional

from .DialogScreenSampler import DialogScreenSampler
from .DialogScreenOCR import DialogScreenOCR
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
        self.__sample = DialogScreenSampler()
        self.__ocr = DialogScreenOCR()
        self.__fuzzy = DialogScreenFuzzy(lang)
        self.__force_parsing = force_parsing
        self.__artifacts_processors = []
        if write_to_dataset:
            self.__artifacts_processors.append(
                DialogScreenDatasetProcessor(playername=playername).process)
        self.__artifacts_processors.append(
            DialogScreenLogger(self.__lang).process)
        self.__prev__title_ocr = None

    def process(self, img: np.ndarray):
        sample_matches = self.__sample.check(img)
        if sample_matches or self.__force_parsing:
            title_ocr, title = self.__ocr.title(img)
            score = self.__fuzzy.title_score(title)
            keys = self.__fuzzy.title_key(title)
            # process artifacts
            for processor in self.__artifacts_processors:
                processor(image=img,
                          dialog_sample_matches=sample_matches,
                          title_ocr=title_ocr,
                          title_fuzzy_score=score,
                          title_keys=keys)
