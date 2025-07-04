from collections import namedtuple
import logging
from typing import Tuple

import cv2
import numpy as np
from typeguard import typechecked

from wa_types import Box, Resolution, is_screenshot

Sample = namedtuple("Sample", "slice, image")


class DialogScreenBaseSampler:
    @typechecked
    def __init__(self,
                 resolution: Resolution,
                 sample_boxes: Tuple[Box, ...]):
        from . import dialog_screen_config
        self._logger = logging.getLogger(type(self).__name__)
        self.__resolution = resolution
        sample_slices = [box.slice for box in sample_boxes]
        blank_image = cv2.imread(dialog_screen_config.screen_blank_img_path)
        self.__samples = [Sample(slice=slice_, image=blank_image[slice_])
                          for slice_ in sample_slices]

    @typechecked
    def check(self, image: np.ndarray) -> bool:
        assert is_screenshot(image, self.__resolution)
        equal = all(np.array_equal(sample.image, image[sample.slice])
                    for sample in self.__samples)
        return equal


class DialogScreenScreenSampler(DialogScreenBaseSampler):
    def __init__(self):
        from wa_screen_manager import config
        from . import dialog_screen_config
        resolution = config.resolution
        sample_boxes = dialog_screen_config.screen_sample_boxes
        # make sure the top and bottom lines will be checked
        assert any(box.t == 0 for box in sample_boxes), \
            "Need to check top line to avoid screen tearing"
        assert any(box.t < resolution.height <= box.b
                   for box in sample_boxes), \
            "Need to check bottom line to avoid screen tearing"
        super().__init__(resolution,
                         sample_boxes)


class DialogScreenRelationSampler(DialogScreenBaseSampler):
    def __init__(self):
        from wa_screen_manager import config
        from . import dialog_screen_config
        resolution = config.resolution
        sample_boxes = dialog_screen_config.relation_sample_boxes
        super().__init__(resolution,
                         sample_boxes)
