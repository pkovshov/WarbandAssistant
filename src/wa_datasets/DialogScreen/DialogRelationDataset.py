from collections import namedtuple
from typing import Optional

import numpy as np
from typeguard import typechecked

from wa_types import Box, Resolution
from wa_datasets.BaseImageDataset import BaseImageDataset, MetaAndImagePath

# TODO: convert to a class with type checking
#       class has to support Mapping type
MetaItem = namedtuple("MetaItem",
                      "verification, "
                      "resolution, "
                      "language, "                      
                      "crop, "
                      "screen_sample_matches, "
                      "relation_ocr, "
                      "relation, "                                        
                      "git_branch, "
                      "git_commit, "
                      "git_has_modified")

# TODO: convert to a class with type checking
#       class has to support Hashable type
MetaKey = namedtuple("MetaKey",
                     "crop, "
                     "relation_ocr, "
                     "screen_sample_matches")


class DialogRelationDataset(BaseImageDataset):
    NAME = "dialog_relations"

    @typechecked
    def __init__(self,
                 resolution: Optional[Resolution] = None,
                 crop: Optional[Box] = None,
                 language: Optional[str] = None,
                 lazy_load: bool = False):
        super().__init__(DialogRelationDataset.NAME, resolution, lazy_load)
        self.__resolution = resolution
        self.__crop = crop
        self.__language = language

    @typechecked
    def meta_and_image_path(self) -> Optional[dict[int, MetaAndImagePath[MetaItem, str]]]:
        return super().meta_and_image_path()

    @typechecked
    def add(self,
            screenshot: np.ndarray,
            screen_sample_matches: bool,
            relation_ocr: str,
            relation: Optional[int]):
        assert self.__resolution is not None
        assert self.__crop is not None
        assert self.__language is not None
        super().add(MetaItem(verification=None,
                             resolution=tuple(self.__resolution),
                             language=self.__language,
                             # yaml does not support saving NamedTuple successors
                             # so need to convert into tuple supported by yaml
                             crop=list(self.__crop),
                             screen_sample_matches=screen_sample_matches,
                             relation_ocr=relation_ocr,
                             relation=relation,
                             git_branch=self.git_status.branch,
                             git_commit=self.git_status.commit,
                             git_has_modified=self.git_status.has_modified),
                    screenshot)

    @typechecked
    def _meta_to_data(self, meta: MetaItem) -> dict:
        return meta._asdict()

    @typechecked
    def _data_to_meta(self, data: dict) -> MetaItem:
        return MetaItem(**data)

    @typechecked
    def _meta_to_key(self, meta: MetaItem) -> MetaKey:
        return MetaKey(
                       # crop is loaded by yaml as a list
                       # and is not hashable for such case
                       # so need to convert into hashable tuple
                       crop=tuple(meta.crop),
                       relation_ocr=meta.relation_ocr,
                       screen_sample_matches=meta.screen_sample_matches)

    @typechecked
    def _preprocess(self, screenshot: np.ndarray) -> np.ndarray:
        assert self.__crop is not None
        return screenshot[self.__crop.slice]
