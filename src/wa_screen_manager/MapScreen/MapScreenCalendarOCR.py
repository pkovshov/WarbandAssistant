import cv2
import numpy as np

from wa_typechecker import typechecked

from wa_screen_manager.BaseScreen.BaseOCR import BaseOCR, NonStable


class MapScreenCalendarOCR(BaseOCR):
    def __init__(self):
        from wa_screen_manager import config
        from . import map_screen_config
        crop_box = map_screen_config.map_calendar_box
        super().__init__(resolution=config.resolution,
                         crop_box=crop_box,
                         whitelist=config.whitelist_characters)

    @typechecked
    def _preprocess(self, crop_img: np.ndarray) -> np.ndarray:
        # grayscale
        img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        # threshold
        _, img = cv2.threshold(img, 117, 255, cv2.THRESH_TRUNC)
        return img
