import logging
from typing import Mapping

import numpy as np
from typeguard import typechecked

from mbw_language import LangValParser

from .DialogScreenOCR import DialogScreenOCR

class DialogScreenManager:
    """DialogScreenManager class

    Responsible for:
    - processing Game Screens
    - ocr Dialog Screens
    - fuzzy ocred strings
    - founding corresponding language keys
    - filling inferred dataset
    """
    @typechecked
    def __init__(self, lang: Mapping[str, LangValParser.Interpolation]):
        self.ocr = DialogScreenOCR()
        self.__prev__title = None
        self.__logger = logging.getLogger(__name__)
        pass

    def process(self, img: np.ndarray):
        title = self.ocr.ocr(img)
        if title != self.__prev__title:
            self.__prev__title = title
            self.__logger.info(title)
