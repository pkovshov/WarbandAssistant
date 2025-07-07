from collections import namedtuple
import logging
from typing import Tuple

import cv2
import numpy as np
from typeguard import typechecked

from wa_types import Box, Resolution, is_screenshot
from wa_screen_manager.BaseScreen.BaseSampler import BaseSampleReadingSampler


class DialogScreenBaseSampler(BaseSampleReadingSampler):
    @typechecked
    def __init__(self,
                 resolution: Resolution,
                 sample_boxes: Tuple[Box, ...]):
        from . import dialog_screen_config
        super().__init__(sample_img_path=dialog_screen_config.dialog_screen_blank_img_path,
                         resolution=resolution,
                         sample_boxes=sample_boxes)


class DialogScreenScreenSampler(DialogScreenBaseSampler):
    def __init__(self):
        from wa_screen_manager import config
        from . import dialog_screen_config
        resolution = config.resolution
        sample_boxes = dialog_screen_config.dialog_screen_sample_boxes
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
