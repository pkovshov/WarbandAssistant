import cv2
import numpy as np

from wa_screen_manager.BaseScreen.BaseOCR import BaseOCR


class MapScreenCalendarOCR(BaseOCR):
    def __init__(self):
        from wa_screen_manager import config
        from . import map_screen_config
        super().__init__(resolution=config.resolution,
                         crop_box=map_screen_config.calendar_box,
                         whitelist=config.whitelist_characters)

    def _preprocess(self, crop_img: np.ndarray) -> np.ndarray:
        # grayscale
        img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        # Otsu threshold
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_TRUNC + cv2.THRESH_OTSU)
        return img
