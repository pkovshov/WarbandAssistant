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
                 sample_boxes: Tuple[Tuple[Box, ...], ...]):
        """
        :param sample_img: A path to sample or blank image
        :param resolution: A screenshots resolution
        :param sample_boxes: Non-empty tuple of several groups, e.g. (A, B, C),
        where each group is a non-empty tuple of Boxes, e.g.
           A = (A1,), B = (B1, B2), C = (C1, C2)
        - A full match (MATCH) occurs if **all boxes in at least one group** match the corresponding sample boxes.
        - A partial match (DOUBT) occurs if **at least one individual box** matches.
        - Otherwise, it's a failed match (FAIL).
        """
        assert is_screenshot(sample_img, resolution)
        assert len(sample_boxes) > 0
        assert all(len(group) > 0 for group in sample_boxes)
        self._logger = logging.getLogger(f"{type(self).__module__}.{type(self).__name__}")
        self.__resolution = resolution
        sample_slices = [[box.slice for box in group] for group in sample_boxes]
        self.__samples = [[Sample(slice=slice_, image=sample_img[slice_])
                           for slice_ in group]
                          for group in sample_slices]

    @typechecked
    def check(self, image: np.ndarray) -> SampleMatch:
        assert is_screenshot(image, self.__resolution)
        is_doubt = False
        for group in self.__samples:
            is_match = True
            for sample in group:
                if np.array_equal(sample.image, image[sample.slice]):
                    is_doubt = True
                    # if current group already does not match,
                    # then we don't need to check other boxes within current group
                    if not is_match:
                        break
                else:
                    is_match = False
                    # if some box already matches
                    # then we don't need to check other boxes within current group
                    if is_doubt:
                        break
            if is_match:
                return SampleMatch.MATCH
        if is_doubt:
            return SampleMatch.DOUBT
        return SampleMatch.FAIL


class BaseSampleReadingSampler(BaseSampler):
    @typechecked
    def __init__(self,
                 sample_img_path: str,
                 resolution: Resolution,
                 sample_boxes: Tuple[Tuple[Box, ...], ...]):
        sample_img = cv2.imread(sample_img_path)
        super().__init__(sample_img,
                         resolution,
                         sample_boxes)
