from abc import ABC, abstractmethod
import logging
from typing import Optional, Tuple

import cv2
import numpy as np
import pytesseract
from typeguard import typechecked

from wa_types import Box, Resolution, is_screenshot
from wa_screen_manager.BaseScreen.BaseOCR import BaseOCR


class DialogScreenTitleOCR(BaseOCR):
    def __init__(self):
        from wa_screen_manager import config
        from . import dialog_screen_config
        crop_box = dialog_screen_config.title_box
        super().__init__(resolution=config.resolution,
                         crop_box=crop_box,
                         whitelist=config.whitelist_characters)
        blank_image = cv2.imread(dialog_screen_config.dialog_screen_blank_img_path)
        blank_image = blank_image[crop_box.slice]
        blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
        self.__blank_img_gray = blank_image
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
        # diff with blank
        img = cv2.absdiff(self.__blank_img_gray, img)
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        img = 255 - img
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img = clahe.apply(img)
        img = cv2.GaussianBlur(img, (13, 13), 0.7)
        return img


class DialogScreenRelationOCR(BaseOCR):
    def __init__(self):
        import path_conf
        from wa_screen_manager import config
        from . import dialog_screen_config
        crop_box = dialog_screen_config.relation_box
        super().__init__(resolution=config.resolution,
                         crop_box=crop_box,
                         whitelist=config.whitelist_numbers)
        blank_image = cv2.imread(dialog_screen_config.dialog_screen_blank_img_path)
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
