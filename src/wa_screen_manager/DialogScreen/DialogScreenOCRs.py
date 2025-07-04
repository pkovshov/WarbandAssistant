from abc import ABC, abstractmethod
import logging
from typing import Optional, Tuple

import cv2
import numpy as np
import pytesseract
from typeguard import typechecked

from wa_types import Box, Resolution, is_screenshot


class DialogScreenBaseOCR(ABC):
    @typechecked
    def __init__(self,
                 resolution: Resolution,
                 crop_box: Box,
                 whitelist: str):
        self._logger = logging.getLogger(type(self).__name__)
        self.__resolution = resolution
        self.__crop_slice = crop_box.slice
        self.__whitelist = whitelist
        self.__prev_crop_img = None
        self.__prev_text_ocr = None

    @typechecked
    def ocr(self, img: np.ndarray) -> str:
        assert is_screenshot(img, self.__resolution)
        crop_img = img[self.__crop_slice]
        if not np.array_equal(crop_img, self.__prev_crop_img):
            self.__prev_crop_img = crop_img
            preprocessed_img = self._preprocess(crop_img)
            text_ocr = self._tesseract_ocr(preprocessed_img)
            self.__prev_text_ocr = text_ocr
            self._logger.debug(f"new image: {repr(text_ocr)}")
        return self.__prev_text_ocr

    @typechecked
    def _tesseract_ocr(self, img: np.ndarray) -> str:
        whitelist = self.__whitelist
        oem = 1
        pcm = 6
        config = f'--oem {oem} --psm {pcm} -c tessedit_char_whitelist="{whitelist}"'
        result = pytesseract.image_to_string(img, config=config)
        result = result.strip()
        result = result.replace('\n', ' ')
        return result

    @abstractmethod
    def _preprocess(self, crop_img: np.ndarray) -> np.ndarray:
        raise NotImplemented


class DialogScreenTitleOCR(DialogScreenBaseOCR):
    def __init__(self):
        from wa_screen_manager import config
        from . import dialog_screen_config
        super().__init__(resolution=config.resolution,
                         crop_box=dialog_screen_config.title_box,
                         whitelist=config.whitelist_characters)
        self.__threshold = dialog_screen_config.title_threshold

    @typechecked
    def title(self, img: np.ndarray) -> Tuple[str, str]:
        title_ocr = self.ocr(img)
        return title_ocr, self._postprocess_title(title_ocr)

    @typechecked
    def _postprocess_title(self, title_ocr: str) -> str:
        # Game adds colon ':' to the end of dialog title
        # Note that colon character is not part of language resources
        return (title_ocr[:-1]
                if len(title_ocr) > 0 and title_ocr[-1] == ":"
                else title_ocr)

    @typechecked
    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        # grayscale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # threshold
        _, img = cv2.threshold(img, self.__threshold, 255, cv2.THRESH_TRUNC)
        return img


class DialogScreenRelationOCR(DialogScreenBaseOCR):
    def __init__(self):
        import path_conf
        from wa_screen_manager import config
        from . import dialog_screen_config
        crop_box = dialog_screen_config.relation_box
        super().__init__(resolution=config.resolution,
                         crop_box=crop_box,
                         whitelist=config.whitelist_numbers)
        blank_image = cv2.imread(dialog_screen_config.screen_blank_img_path)
        blank_image = blank_image[crop_box.slice]
        blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
        self.__blank_img_gray = blank_image

    @typechecked
    def relation(self, img: np.ndarray) -> Tuple[str, Optional[int]]:
        relation_ocr = self.ocr(img)
        return relation_ocr, self._postprocess_relation(relation_ocr)

    @typechecked
    def _postprocess_relation(self, relation_ocr: str) -> Optional[int]:
        try:
            return int(relation_ocr)
        except ValueError:
            return None

    @typechecked
    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        # grayscale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # diff with blank
        img = cv2.absdiff(self.__blank_img_gray, img)
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        img = 255 - img
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img = clahe.apply(img)
        img = cv2.GaussianBlur(img, (13, 13), 0.7)
        return img

