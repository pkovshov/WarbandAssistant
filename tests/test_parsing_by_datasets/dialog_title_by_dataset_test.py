import cv2
from os import path
from typing import Any

import pytest

import path_conf
from wa_config import screen_conf
from wa_types import LanguageCode
from wa_language import Language
from wa_language.LanguageModel import LanguageModel
from wa_datasets.DialogTitlesDataset import (DialogTitlesDataset,
                                             VERIFICATION_NOT_A_DIALOG_TITLE)
from wa_screen_manager.DialogScreen.DialogScreenOCRs import DialogScreenTitleOCR
from wa_screen_manager.DialogScreen.DialogScreenTitleFuzzyParser import DialogScreenTitleFuzzyParser
from .base_dataset_staff import load_idxes_and_metas_by_langcode, lazy_image_value

blank_image = cv2.imread(path.join(path_conf.samples, "dialog_screen_blank.png"))

dataset = DialogTitlesDataset(lazy_load=True)

idxes_and_metas_by_langcode = load_idxes_and_metas_by_langcode(dataset)

ocrs_and_parsers_by_lang_code: dict[LanguageCode, tuple[Any, Any]] = dict()
for langcode in idxes_and_metas_by_langcode:
    language = Language.load(langcode)
    ocr = DialogScreenTitleOCR(language_code=langcode,
                               whitelist=screen_conf.ALPHABET[langcode] +
                                         screen_conf.PUNCTUATION +
                                         screen_conf.DIGITS)
    parser = DialogScreenTitleFuzzyParser(language)
    ocrs_and_parsers_by_lang_code[langcode] = (ocr, parser)

params = []

for langcode, idxes_and_metas in idxes_and_metas_by_langcode.items():
    ocr, parser = ocrs_and_parsers_by_lang_code[langcode]
    for idx, meta in idxes_and_metas:
        if meta.verification == VERIFICATION_NOT_A_DIALOG_TITLE:
            continue
        if meta.sample_matches is False:
            continue
        if "wa_player" in meta.keys:
            continue
        params.append((idx,
                       meta,
                       lazy_image_value(dataset, idx, meta, blank_image),
                       ocr,
                       parser))


@pytest.mark.parametrize("idx,"
                         "meta,"
                         "image,"
                         "ocr,"
                         "parser",
                         params)
def test_dialog_title_dataset(idx, meta, image, ocr, parser):
    ocr.ocr(image)  # Dry run to simulate two identical images in a row
    title_ocr = ocr.ocr(image)
    title_keys = parser.keys(title_ocr)
    assert title_keys == tuple(meta.keys), f"OCR: {title_ocr}"
