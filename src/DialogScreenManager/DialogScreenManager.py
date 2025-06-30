import logging
from typing import Mapping

from mbw_language import LangValParser
import numpy as np
from typeguard import typechecked
from typing import Optional

from .DialogScreenOCR import DialogScreenOCR
from .DialogScreenFuzzy import DialogScreenFuzzy
from .DialogScreenDataset import DialogScreenDataset
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
                 playername: Optional[str] = None):
        self.__logger = logging.getLogger(__name__)
        self.__lang = lang
        self.__ocr = DialogScreenOCR()
        self.__fuzzy = DialogScreenFuzzy(lang)
        self.__dataset = DialogScreenDataset(playername=playername) if write_to_dataset else None
        self.__prev__title_ocr = None

        pass

    def process(self, img: np.ndarray):
        title_ocr = self.__ocr.title(img)
        if title_ocr != self.__prev__title_ocr:
            self.__prev__title_ocr = title_ocr
            title = title_ocr.strip()
            if len(title) > 0 and title[-1] == ":":
                title = title[:-1]
            title_keys = self.__fuzzy.title_key(title)
            if title_keys:
                if self.__dataset is not None:
                    self.__dataset.process(img=img,
                                           title_ocr=title_ocr,
                                           title_fuzzy_score=self.__fuzzy.title_score(title),
                                           title_keys=title_keys)
                title_key = title_keys[0]
                val = self.__lang[title_key]
                if DialogScreenModel.is_king(title_key):
                    text = f"Ruler {val}"
                elif DialogScreenModel.is_lord(title_key):
                    text = f"Lord {val}"
                elif DialogScreenModel.is_lady(title_key):
                    text = f"Lady {val}"
                else:
                    text = val
                self.__logger.info(text)
