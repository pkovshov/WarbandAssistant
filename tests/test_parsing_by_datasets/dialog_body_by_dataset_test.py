from functools import partial
from os import path
from typing import Any, Mapping, NamedTuple

import cv2
import pytest
from pytest_cases import lazy_value

import path_conf
from wa_model.dialog_model.DialogBodyModel import DialogBodyModel
from wa_types import Box, LanguageCode
from wa_language import Language
from wa_language.Language import LangKey
from wa_language.LangVar import PlayerSex
from wa_datasets.DialogBodiesDataset import DialogBodiesDataset, keys_and_bindings
from wa_screen_manager.DialogScreen.DialogScreenOCRs import DialogBodyOCR
from wa_screen_manager.DialogScreen.DialogBodyFuzzyParser import DialogBodyFuzzyParser
from .base_dataset_staff import load_idxes_and_metas_by_langcode_and_playersex, lazy_image_value

blank_image = cv2.imread(path.join(path_conf.samples, "dialog_screen_blank.png"))

dataset = DialogBodiesDataset(lazy_load=True)

idxes_and_metas_by_langcode_and_playersex = load_idxes_and_metas_by_langcode_and_playersex(dataset)


language_by_langcode = dict()
ocrs_and_parsers_by_langcode_and_playersex: dict[tuple[LanguageCode, PlayerSex], tuple[Any, Any]] = dict()
for langcode_and_playersex in idxes_and_metas_by_langcode_and_playersex:
    langcode, playersex = langcode_and_playersex
    if langcode not in language_by_langcode:
        language_by_langcode[langcode] = Language.load(langcode)
    language = language_by_langcode[langcode]
    model = DialogBodyModel(language=language,
                            player_name=None,
                            player_sex=playersex)
    ocr = DialogBodyOCR(language_code=langcode,
                        whitelist=model.symbols)
    parser = DialogBodyFuzzyParser(model)
    ocrs_and_parsers_by_langcode_and_playersex[langcode_and_playersex] = (ocr, parser)

params = []

for langcode_and_playersex, idxes_and_metas in idxes_and_metas_by_langcode_and_playersex.items():
    ocr, parser = ocrs_and_parsers_by_langcode_and_playersex[langcode_and_playersex]
    for idx, meta in idxes_and_metas:
        params.append((idx,
                       meta.body_ocr,
                       tuple(LangKey(key) for key in meta.title_keys),
                       meta.body_bounds,
                       lazy_image_value(dataset, idx, meta, blank_image),
                       ocr,
                       parser))


@pytest.mark.parametrize("idx,"
                         "body_ocr_exp,"
                         "title_keys,"
                         "body_bounds_exp,"
                         "image,"
                         "ocr,"
                         "parser",
                         params)
def test_male_dialog_body_dataset(idx, body_ocr_exp, title_keys, body_bounds_exp, image, ocr, parser):
    ocr.ocr(image)  # Dry run to simulate two identical images in a row
    body_ocr = ocr.ocr(image)
    body_bounds = parser.bounds(body_ocr, title_keys)
    body_bounds = keys_and_bindings(body_bounds)
    assert body_bounds == body_bounds_exp, f"OCR: {body_ocr}"
