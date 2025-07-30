import cv2
from functools import partial
from os import path

import pytest
from pytest_cases import lazy_value

import path_conf
from wa_types import Box
from wa_language import Language
from wa_language.Language import LangKey
from wa_language.LangVar import PlayerSex
from wa_datasets.DialogBodiesDataset import DialogBodiesDataset
from wa_screen_manager.DialogScreen.DialogScreenEvent import DialogBodyBound
from wa_screen_manager.DialogScreen.DialogScreenOCRs import DialogBodyOCR
from wa_screen_manager.DialogScreen.DialogBodyFuzzyParser import DialogBodyFuzzyParser


blank = cv2.imread(path.join(path_conf.samples, "dialog_screen_blank.png"))


lang = Language.load()

dataset = DialogBodiesDataset(lazy_load=True)

ocr = DialogBodyOCR()

male_parser = DialogBodyFuzzyParser(lang, PlayerSex.MALE)
female_parser = DialogBodyFuzzyParser(lang, PlayerSex.FEMALE)

male_params = []
female_params = []


def load_image(idx, meta):
    crop = Box(*meta.crop)
    mask = Box(*meta.mask)
    blank_copy = blank.copy()
    image = cv2.imread(dataset.img_path(idx))
    blank_copy[(mask + crop.point).slice] = image[mask.slice]
    return blank_copy


def load_test_arguments(idx, meta):
    return [idx,
            meta.body_ocr,
            tuple(LangKey(key) for key in meta.title_keys),
            sorted(list(DialogBodyBound(key=LangKey(bound[0]),
                                        bind=dict(bound[1]))
                        for bound in meta.body_bounds),
                   key=lambda bound: bound.key),
            lazy_value(partial(load_image, idx=idx, meta=meta))]


for idx, meta in dataset.meta_dict.items():
    argumets = load_test_arguments(idx=idx, meta=meta)
    if meta.playersex == 'male':
        male_params.append(argumets + [male_parser])
    elif meta.playersex == 'female':
        female_params.append(argumets + [female_parser])


@pytest.mark.parametrize("idx, body_ocr_exp, title_keys, body_bounds_exp, image, parser", male_params + female_params)
def test_male_dialog_body_dataset(idx, body_ocr_exp, title_keys, body_bounds_exp, image, parser):
    ocr.ocr(image)  # Dry run to simulate two identical images in a row
    body_ocr = ocr.ocr(image)
    body_bounds = parser.bound(body_ocr, title_keys)
    assert sorted(body_bounds, key=lambda bound: bound.key) == body_bounds_exp, f"OCR: {body_ocr}"
