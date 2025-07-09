import cv2
import numpy as np
import pytest

from wa_language.LangLoader import load_lang
from wa_datasets.DialogScreen.DialogRelationDataset import DialogRelationDataset
from wa_screen_manager.DialogScreen.DialogScreenOCRs import DialogScreenRelationOCR
from wa_screen_manager.DialogScreen.DialogScreenRelationParser import DialogScreenRelationParser


def load_image_and_restore_crop(image_path, resolution, crop):
    width, height = resolution
    result = np.zeros((height, width, 3), dtype=np.uint8)
    image = cv2.imread(image_path)
    result[crop[1]: crop[3],
           crop[0]: crop[2]] = image
    return result


lang = load_lang()

dataset = DialogRelationDataset(lazy_load=True)

ocr = DialogScreenRelationOCR()

parser = DialogScreenRelationParser()

idx_meta_image = []

for idx, (meta, image_path) in dataset.meta_and_image_path().items():
    image = load_image_and_restore_crop(image_path,
                                        meta.resolution,
                                        meta.crop)
    idx_meta_image.append((dataset.idx_to_stem(idx), meta.relation_ocr, meta.relation, image))


@pytest.mark.parametrize("idx, relation_ocr_exp, relation_exp, image", idx_meta_image)
def test_dialog_title_dataset(idx, relation_ocr_exp, relation_exp, image):
    ocr.ocr(image)  # Dry run to simulate two identical images in a row
    relation_ocr = ocr.ocr(image)
    relation = parser.relation(relation_ocr)
    assert relation_ocr == relation_ocr_exp, f"OCR: {relation_ocr}"
    assert relation == relation_exp, f"OCR: {relation_ocr}"
    assert relation is not None, f"OCR: {relation_ocr}"
