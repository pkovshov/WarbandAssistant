from collections import namedtuple
from os import path
from typing import Any, List, Mapping, NamedTuple, Optional, Tuple

import cv2
import numpy as np
from wa_typechecker import typechecked

import path_conf
from wa_language.model.types import PlayerSex
from wa_types import Box, Resolution
from wa_language.Language import LangKey
from wa_datasets.BaseImageDataset import BaseImageDataset, MetaAndImagePath

# TODO: convert to a class with type checking
#       class has to support Mapping type
MetaItem = namedtuple("MetaItem",
                      "verification, "
                      "resolution, "
                      "language, "
                      "playername, "
                      "playersex, "
                      "crop, "
                      "mask, "
                      "screen_sample_matches, "
                      "title_keys, "
                      "body_ocr, "
                      "body_bounds, "                         
                      "git_branch, "
                      "git_commit, "
                      "git_has_modified")

class MetaKey(NamedTuple):
    crop: Box
    mask: Box
    body_ocr: str

    def __eq__(self, other):
        if not isinstance(other, MetaKey):
            return False
        return (other.mask + other.crop.point in self.crop and
                self.mask + self.crop.point in other.crop)

    def __hash__(self):
        return hash(self.body_ocr)


class DialogBodiesDataset(BaseImageDataset):
    NAME = "dialog_bodies"

    @typechecked
    def __init__(self,
                 resolution: Optional[Resolution] = None,
                 crop: Optional[Box] = None,
                 language: Optional[str] = None,
                 player_name: Optional[str] = None,
                 player_sex: Optional[PlayerSex] = None,
                 blank_img_path: Optional[str] = None,
                 lazy_load: bool = False):
        super().__init__(self.NAME,
                         # Hack to avoid assert on is_screenshot check in BaseImageDataset.add(...) method
                         crop.resolution if crop else None,
                         lazy_load)
        self.__resolution = resolution
        self.__crop = crop
        self.__language = language
        self.__player_name = player_name
        self.__player_sex = player_sex
        self.__blank = None
        if crop is not None and blank_img_path is not None:
            blank_image = cv2.imread(blank_img_path)
            self.__blank = blank_image[crop.slice]

    @typechecked
    def meta_and_image_path(self) -> Optional[dict[int, MetaAndImagePath[MetaItem, str]]]:
        return super().meta_and_image_path()

    @staticmethod
    def pack_body_bounds(body_bounds: Tuple[Tuple[LangKey, Mapping[str, Any]], ...]):
        result = []
        for bound in body_bounds:
            key = str(bound[0])
            bind = {str(key):str(val) for key, val in bound[1].items()}
            result.append([key, bind])
        return result

    @typechecked
    def add(self,
            screenshot: np.ndarray,
            screen_sample_matches: bool,
            title_keys: Tuple[LangKey, ...],
            body_ocr: Optional[str],
            body_bounds
            ):
        if not body_bounds:
            return
        assert self.__resolution is not None
        assert self.__crop is not None
        assert self.__language is not None
        img, mask = self.do_crop(screenshot)
        # # Hack to avoid assert on is_screenshot check in BaseImageDataset.add(...) method
        # self._BaseImageDataset__resolution = mask.resolution
        # # Add meta and cropped screenshot
        super().add(MetaItem(verification=None,
                             resolution=tuple(self.__resolution),
                             language=self.__language,
                             playername=self.__player_name,
                             playersex=self.__player_sex.value if self.__player_sex else None,
                             # yaml does not support saving NamedTuple successors
                             # so need to convert into tuple supported by yaml
                             crop=tuple(self.__crop),
                             mask=tuple(mask),
                             screen_sample_matches=screen_sample_matches,
                             title_keys=tuple(str(key) for key in title_keys),
                             body_ocr=body_ocr,
                             body_bounds=self.pack_body_bounds(body_bounds),
                             git_branch=self.git_status.branch,
                             git_commit=self.git_status.commit,
                             git_has_modified=self.git_status.has_modified),
                    img)

    @typechecked
    def _meta_to_data(self, meta: MetaItem) -> dict:
        return meta._asdict()

    @typechecked
    def _data_to_meta(self, data: dict) -> MetaItem:
        return MetaItem(**data)

    @typechecked
    def _meta_to_key(self, meta: MetaItem) -> Tuple[MetaKey, bool]:
        return (MetaKey(crop=Box(*meta.crop),
                        mask=Box(*meta.mask),
                        body_ocr=meta.body_ocr),
                # is_soft_key
                False)

    @typechecked
    def do_crop(self, screenshot: np.ndarray) -> Tuple[np.ndarray, Box]:
        assert self.__crop is not None
        assert self.__blank is not None
        blank = self.__blank
        image = screenshot[self.__crop.slice]
        image_copy = image.copy()
        # from left and right edges to the middle
        height = self.__crop.resolution.height
        right = self.__crop.resolution.width
        middle = right // 2
        width = middle // 2
        left = 0
        while width >= 1:
            left_box = Box(l=left,
                           t=0,
                           r=left+width,
                           b=height)
            right_box = Box(l=right-width,
                            t=0,
                            r=right,
                            b=height)
            if np.array_equal(image[left_box.slice], blank[left_box.slice]):
                left = left_box.r
            if np.array_equal(image[right_box.slice], blank[right_box.slice]):
                right = right_box.l
            width = width // 2
        # crop image and blank
        crop = Box(l=left,
                   t=0,
                   r=right,
                   b=height)
        image = image[crop.slice]
        blank = blank[crop.slice]
        # from bottom edge to the top one
        width = crop.resolution.width
        bottom = crop.resolution.height
        height = bottom // 2
        while height >= 1:
            bottom_box = Box(l=0,
                             t=bottom-height,
                             r=width,
                             b=bottom)
            if np.array_equal(image[bottom_box.slice], blank[bottom_box.slice]):
                bottom = bottom_box.t
            height = height // 2
        # from top edge check line by line
        top = 0
        for _ in range(20):
            top_box = Box(l=0,
                          t=top,
                          r=width,
                          b=top+1)
            if np.array_equal(image[top_box.slice], blank[top_box.slice]):
                top += 1
        # build mask and update image
        mask = Box(l=left,
                   t=top,
                   r=right,
                   b=bottom)
        image_copy[:top, :] = 0
        image_copy[bottom:, :] = 0
        image_copy[:bottom, :left] = 0
        image_copy[:bottom, right:] = 0
        return image_copy, mask

    @typechecked
    def _preprocess(self, screenshot: np.ndarray) -> np.ndarray:
        return screenshot
