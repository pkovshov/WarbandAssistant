from os import path

import cv2
import numpy as np
import pytest

import path_conf
from wa_types import Box, LanguageCode
from wa_language import Language
from wa_datasets.DialogRelationsDataset import DialogRelationsDataset
from wa_screen_manager.DialogScreen.DialogScreenOCRs import DialogScreenRelationOCR
from wa_screen_manager.DialogScreen.DialogScreenRelationParser import DialogScreenRelationParser
from .base_dataset_staff import lazy_image_value


blank_image = cv2.imread(path.join(path_conf.samples, "dialog_screen_blank.png"))

lang = Language.load(LanguageCode.EN)

dataset = DialogRelationsDataset(lazy_load=True)

ocr = DialogScreenRelationOCR(LanguageCode.EN)

parser = DialogScreenRelationParser()

idx_meta_image = []

for idx, meta in dataset.meta_dict.items():
    idx_meta_image.append((dataset.idx_to_stem(idx),
                           meta.relation_ocr,
                           meta.relation,
                           lazy_image_value(dataset, idx, meta, blank_image)))


@pytest.mark.parametrize("idx, relation_ocr_exp, relation_exp, image", idx_meta_image)
def test_dialog_title_dataset(idx, relation_ocr_exp, relation_exp, image):
    ocr.ocr(image)  # Dry run to simulate two identical images in a row
    relation_ocr = ocr.ocr(image)
    relation = parser.relation(relation_ocr)
    assert relation == relation_exp, f"OCR: {repr(relation_ocr)}"
    assert relation is not None, f"OCR: {repr(relation_ocr)}"
