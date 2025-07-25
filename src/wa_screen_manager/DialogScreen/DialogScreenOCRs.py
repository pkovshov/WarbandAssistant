from typing import Optional, Union, Tuple

import cv2
import numpy as np
from wa_typechecker import typechecked

from wa_screen_manager.BaseScreen.BaseOCR import BaseOCR, NonStableType, NonStable


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

    def ocr(self, img: np.ndarray) -> Union[str, NonStableType]:
        title_ocr = super().ocr(img)
        if title_ocr == "Emir Ugqais:":
            return "Emir Uqais:"
        return title_ocr

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


class DialogBodyOCR(BaseOCR):
    def __init__(self):
        from wa_screen_manager import config
        from . import dialog_screen_config
        crop_box = dialog_screen_config.body_box
        super().__init__(resolution=config.resolution,
                         crop_box=crop_box,
                         whitelist=config.whitelist_characters)
        blank_image = cv2.imread(dialog_screen_config.dialog_screen_blank_img_path)
        blank_image = blank_image[crop_box.slice]
        blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
        self.__blank_img_gray = blank_image

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
