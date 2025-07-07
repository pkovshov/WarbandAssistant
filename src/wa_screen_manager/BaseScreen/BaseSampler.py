from collections import namedtuple
import logging
from typing import Tuple

import cv2
import numpy as np
from typeguard import typechecked

from wa_types import Box, Resolution, is_screenshot
from wa_screen_manager.SampleMatch import SampleMatch


Sample = namedtuple("Sample", "slice, image")


class BaseSampler:
    @typechecked
    def __init__(self,
                 sample_img: np.ndarray,
                 resolution: Resolution,
                 sample_boxes: Tuple[Box, ...]):
        assert is_screenshot(sample_img, resolution)
        self._logger = logging.getLogger(f"{type(self).__module__}.{type(self).__name__}")
        self.__resolution = resolution
        sample_slices = [box.slice for box in sample_boxes]
        self.__samples = [Sample(slice=slice_, image=sample_img[slice_])
                          for slice_ in sample_slices]

    @typechecked
    def check(self, image: np.ndarray) -> SampleMatch:
        assert is_screenshot(image, self.__resolution)
        matches = [np.array_equal(sample.image, image[sample.slice])
                   for sample in self.__samples]
        if all(matches):
            return SampleMatch.MATCH
        elif any(matches):
            return SampleMatch.DOUBT
        else:
            return SampleMatch.FAIL


class BaseSampleReadingSampler(BaseSampler):
    @typechecked
    def __init__(self,
                 sample_img_path: str,
                 resolution: Resolution,
                 sample_boxes: Tuple[Box, ...]):
        sample_img = cv2.imread(sample_img_path)
        super().__init__(sample_img,
                         resolution,
                         sample_boxes)
