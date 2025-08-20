from collections import defaultdict
from functools import partial
from typing import Any

import cv2
import numpy as np
from pytest_cases import lazy_value

from wa_language.LangVar import PlayerSex
from wa_types import Box, LanguageCode
from wa_datasets import BaseImageDataset


def load_idxes_and_metas_by_langcode(dataset: BaseImageDataset) -> dict[LanguageCode, tuple[int, Any]]:
    idxes_and_metas_by_language_code = defaultdict(list)
    for idx, meta in dataset.meta_dict.items():
        idxes_and_metas_by_language_code[LanguageCode(meta.language)].append((idx, meta))
    return idxes_and_metas_by_language_code


def load_idxes_and_metas_by_langcode_and_playersex(dataset: BaseImageDataset) -> dict[tuple[LanguageCode, PlayerSex], tuple[int, Any]]:
    idxes_and_metas_by_langcode_and_playersex = defaultdict(list)
    for idx, meta in dataset.meta_dict.items():
        idxes_and_metas_by_langcode_and_playersex[(LanguageCode(meta.language), PlayerSex(meta.playersex))].append((idx, meta))
    return idxes_and_metas_by_langcode_and_playersex


def load_image(image_path, meta, blank_image: np.ndarray):
    blank_copy = blank_image.copy()
    image = cv2.imread(image_path)
    crop = Box(*meta.crop)
    mask = Box(*meta.mask) if hasattr(meta, "mask") else Box(image)
    blank_copy[(mask + crop.point).slice] = image[mask.slice]
    return blank_copy

def lazy_image_value(dataset: BaseImageDataset, idx, meta, blank_image):
    return lazy_value(partial(load_image,
                              image_path = dataset.img_path(idx),
                              meta = meta,
                              blank_image = blank_image))

