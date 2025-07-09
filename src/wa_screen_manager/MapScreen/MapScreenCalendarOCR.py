import cv2
import numpy as np

from typeguard import typechecked

from wa_screen_manager.BaseScreen.BaseOCR import BaseOCR


class MapScreenCalendarOCR(BaseOCR):
    def __init__(self):
        from wa_screen_manager import config
        from . import map_screen_config
        crop_box = map_screen_config.calendar_box
        super().__init__(resolution=config.resolution,
                         crop_box=crop_box,
                         whitelist=config.whitelist_characters)
        blank_image = cv2.imread(map_screen_config.map_screen_blank_img_path)
        blank_image = blank_image[crop_box.slice]
        blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
        self.__blank_img_gray = blank_image

    @typechecked
    def _preprocess(self, crop_img: np.ndarray) -> np.ndarray:
        # grayscale
        img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        # threshold
        _, img = cv2.threshold(img, 117, 255, cv2.THRESH_TRUNC)
        return img
