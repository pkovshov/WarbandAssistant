from collections import namedtuple
import logging

import cv2
import numpy as np
from typeguard import typechecked


Sample = namedtuple("Sample", "slice, image")


class DialogScreenSampler:
    def __init__(self):
        # create logger
        self.__logger = logging.getLogger(__name__)
        # process configs
        from wa_screen_manager import config
        from . import dialog_screen_sampler_config
        resolution = config.resolution
        self.__resolution = config.resolution
        # load sample boxes
        sample_boxes = dialog_screen_sampler_config.sample_boxes
        # make sure the top and bottom lines will be checked
        assert any(box.t == 0 for box in sample_boxes), \
            "Need to check top line to avoid screen tearing"
        assert any(box.t < resolution.height <= box.b
                   for box in sample_boxes), \
            "Need to check bottom line to avoid screen tearing"
        # build slices
        sample_slices = [(slice(box.t, box.b),
                          slice(box.l, box.r))
                         for box in sample_boxes]
        # for each slice load samples from blank
        blank_img = cv2.imread(dialog_screen_sampler_config.blank_img_path)
        self.__samples = [Sample(slice=slice_, image=blank_img[slice_])
                          for slice_ in sample_slices]

    @typechecked
    def check(self, img: np.ndarray) -> bool:
        assert img.dtype == np.uint8
        assert img.ndim == 3
        assert img.shape[0] == self.__resolution.height
        assert img.shape[1] == self.__resolution.width
        assert img.shape[2] == 3
        equal = all(np.array_equal(sample.image, img[sample.slice])
                    for sample in self.__samples)
        return equal
