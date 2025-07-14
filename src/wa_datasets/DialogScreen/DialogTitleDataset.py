from collections import namedtuple
from typing import Mapping, Optional, Tuple

import numpy as np
from typeguard import typechecked

from wa_types import Box, Resolution
from wa_datasets.BaseImageDataset import BaseImageDataset, MetaAndImagePath


VERIFICATION_NOT_A_DIALOG_TITLE = "Not a dialog title"

# TODO: convert to a class with type checking
#       class has to support Mapping type
MetaItem = namedtuple("MetaItem",
                      "verification, "
                      "resolution, "
                      "language, "
                      "playername, "
                      "crop, "
                      "sample_matches, "
                      "title_ocr, "
                      "fuzzy_score, "
                      "keys, "                         
                      "git_branch, "
                      "git_commit, "
                      "git_has_modified")

# TODO: convert to a class with type checking
#       class has to support Hashable type
MetaKey = namedtuple("MetaKey",
                     "crop, "
                     "title_ocr, "
                     "sample_matches")


class DialogTitleDataset(BaseImageDataset):
    NAME = "dialog_titles"

    @typechecked
    def __init__(self,
                 resolution: Optional[Resolution] = None,
                 crop: Optional[Box] = None,
                 language: Optional[str] = None,
                 playername: Optional[str] = None,
                 lazy_load: bool = False):
        super().__init__(DialogTitleDataset.NAME, resolution, lazy_load)
        self.__resolution = resolution
        self.__crop = crop
        self.__language = language
        self.__playername = playername

    @typechecked
    def meta_and_image_path(self) -> Optional[dict[int, MetaAndImagePath[MetaItem, str]]]:
        return super().meta_and_image_path()

    @typechecked
    def add(self,
            screenshot: np.ndarray,
            sample_matches: bool,
            title_ocr: str,
            title_fuzzy_score: Optional[float],
            title_keys: Tuple[str, ...]):
        assert self.__resolution is not None
        assert self.__crop is not None
        assert self.__language is not None
        super().add(MetaItem(verification=None,
                             resolution=tuple(self.__resolution),
                             language=self.__language,
                             playername=self.__playername,
                             # yaml does not support saving NamedTuple successors
                             # so need to convert into tuple supported by yaml
                             crop=list(self.__crop),
                             sample_matches=sample_matches,
                             title_ocr=title_ocr,
                             fuzzy_score=title_fuzzy_score,
                             keys=title_keys,
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
    def _meta_to_key(self, meta: MetaItem) -> Tuple[MetaKey, bool]:
        return (MetaKey(
                        # crop is loaded by yaml as a list
                        # and is not hashable for such case
                        # so need to convert into hashable tuple
                        crop=tuple(meta.crop),
                        title_ocr=meta.title_ocr,
                        sample_matches=meta.sample_matches),
                # is_soft_key
                False)

    @typechecked
    def _preprocess(self, screenshot: np.ndarray) -> np.ndarray:
        assert self.__crop is not None
        return screenshot[self.__crop.slice]
