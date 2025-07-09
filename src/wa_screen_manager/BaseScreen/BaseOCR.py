from abc import ABC, abstractmethod
from enum import Enum
import logging
from typing import Union

import numpy as np
import pytesseract
from typeguard import typechecked

from wa_types import Box, Resolution, is_screenshot


class NonStableType(Enum):
    NonStable = "NonStable"


NonStable = NonStableType.NonStable


class BaseOCR(ABC):
    @typechecked
    def __init__(self,
                 resolution: Resolution,
                 crop_box: Box,
                 whitelist: str):
        self._logger = logging.getLogger(f"{type(self).__module__}.{type(self).__name__}")
        self.__resolution = resolution
        self.__crop_slice = crop_box.slice
        self.__whitelist = whitelist
        self.__prev_crop_img = None
        self.__prev_text_ocr = None

    @typechecked
    def ocr(self, img: np.ndarray) -> Union[str, NonStableType]:
        assert is_screenshot(img, self.__resolution)
        crop_img = img[self.__crop_slice]
        if not np.array_equal(crop_img, self.__prev_crop_img):
            self.__prev_text_ocr = NonStable
        elif self.__prev_text_ocr is NonStable:
            preprocessed_img = self._preprocess(crop_img)
            text_ocr = self._tesseract_ocr(preprocessed_img)
            self.__prev_text_ocr = text_ocr
        self.__prev_crop_img = crop_img
        return self.__prev_text_ocr

    @typechecked
    def _tesseract_ocr(self, img: np.ndarray) -> str:
        whitelist = self.__whitelist
        oem = 1
        pcm = 6
        config = f'--oem {oem} --psm {pcm} -c tessedit_char_whitelist="{whitelist}"'
        result = pytesseract.image_to_string(img, config=config)
        result = result.strip()
        return result

    @abstractmethod
    def _preprocess(self, crop_img: np.ndarray) -> np.ndarray:
        raise NotImplemented
