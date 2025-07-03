import logging

import cv2
import numpy as np
import pytesseract
from typeguard import typechecked


class DialogScreenOCR:
    def __init__(self):
        from wa_screen_manager import config
        from . import dialog_screen_config
        self.__logger = logging.getLogger(__name__)
        self.__whitelist = config.whitelist_characters
        self.__resolution = config.resolution
        title_box = dialog_screen_config.title_box
        self.__title_slice = (slice(title_box.t, title_box.b),
                              slice(title_box.l, title_box.r))
        self.__prev_title_img = None
        self.__prev_title_ocr = None
        pass

    @typechecked
    def title(self, img: np.ndarray) -> str:
        assert img.dtype == np.uint8
        assert img.ndim == 3
        assert img.shape[0] == self.__resolution.height
        assert img.shape[1] == self.__resolution.width
        assert img.shape[2] == 3
        # crop
        title_img = img[self.__title_slice]
        if not np.array_equal(title_img, self.__prev_title_img):
            self.__prev_title_img = title_img
            title_img = self._preprocess_title(title_img)
            title_ocr = self._tesseract_ocr(title_img)
            self.__prev_title_ocr = title_ocr
            self.__logger.debug(f"new image: {repr(title_ocr)}")
        return self.__prev_title_ocr

    @typechecked
    def _preprocess_title(self, img: np.ndarray) -> np.ndarray:
        # grayscale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Otsu threshold
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_TRUNC + cv2.THRESH_OTSU)
        return img

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
