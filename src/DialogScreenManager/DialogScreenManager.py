import logging
from typing import Mapping

from mbw_language import LangValParser
import numpy as np
from typeguard import typechecked
from typing import Optional

from .DialogScreenSampler import DialogScreenSampler
from .DialogScreenOCR import DialogScreenOCR
from .DialogScreenFuzzy import DialogScreenFuzzy
from .DialogScreenDatasetProcessor import DialogScreenDatasetProcessor
from .DialogScreenLogger import DialogScreenLogger
from . import DialogScreenModel


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
        self.__artifacts = []
        if write_to_dataset:
            self.__artifacts.append(DialogScreenDatasetProcessor(playername=playername))
        self.__artifacts.append(DialogScreenLogger(self.__lang))
        self.__prev__title_ocr = None

    def process(self, img: np.ndarray):
        sample_matches = self.__sample.check(img)
        if sample_matches or self.__force_parsing:
            title_ocr = self.__ocr.title(img)
            # Game adds colon ':' to the end of dialog title
            # Note that colon character is not part of language resources
            title = title_ocr.strip()
            if len(title) > 0 and title[-1] == ":":
                title = title[:-1]
            # process artifacts
            for processor in self.__artifacts:
                processor.process(img=img,
                                  sample_matches=sample_matches,
                                  title_ocr=title_ocr,
                                  title_fuzzy_score=self.__fuzzy.title_score(title),
                                  title_keys=self.__fuzzy.title_key(title))
