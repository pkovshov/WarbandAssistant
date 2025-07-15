import cv2
import numpy as np
import pytest

from wa_language import Lang
from wa_datasets.DialogScreen.DialogTitleDataset import (DialogTitleDataset,
                                                         VERIFICATION_NOT_A_DIALOG_TITLE)
from wa_screen_manager.DialogScreen.DialogScreenOCRs import DialogScreenTitleOCR
from wa_screen_manager.DialogScreen.DialogScreenTitleFuzzyParser import DialogScreenTitleFuzzyParser


def load_image_and_restore_crop(image_path, resolution, crop):
    width, height = resolution
    result = np.zeros((height, width, 3), dtype=np.uint8)
    image = cv2.imread(image_path)
    result[crop[1]: crop[3],
           crop[0]: crop[2]] = image
    return result


lang = Lang.load()

dataset = DialogTitleDataset(lazy_load=True)

ocr = DialogScreenTitleOCR()

parser = DialogScreenTitleFuzzyParser(lang)

idx_meta_image = []

for idx, (meta, image_path) in dataset.meta_and_image_path().items():
    if meta.verification == VERIFICATION_NOT_A_DIALOG_TITLE:
        continue
    if meta.sample_matches is False:
        continue
    if "wa_player" in meta.keys:
        continue
    image = load_image_and_restore_crop(image_path,
                                        meta.resolution,
                                        meta.crop)
    idx_meta_image.append((dataset.idx_to_stem(idx), meta, image))


@pytest.mark.parametrize("idx, meta, image", idx_meta_image)
def test_dialog_title_dataset(idx, meta, image):
    ocr.ocr(image)  # Dry run to simulate two identical images in a row
    title_ocr = ocr.ocr(image)
    title_keys = parser.keys(title_ocr)
    assert title_keys == tuple(meta.keys), f"OCR: {title_ocr}"
