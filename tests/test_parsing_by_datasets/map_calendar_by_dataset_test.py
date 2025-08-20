from os import path
from typing import Any, NamedTuple

import cv2
import numpy as np
import pytest

import path_conf
from wa_types import LanguageCode
from wa_language import Language
from wa_language.LanguageModel import LanguageModel
from wa_model import calendar_model
from wa_screen_manager.MapScreen.MapScreenCalendarOCR import MapScreenCalendarOCR
from wa_screen_manager.MapScreen.MapScreenCalendarFuzzyParser import MapScreenCalendarFuzzyParser
from wa_datasets.MapCalendarsDataset import (MapCalendarsDataset,
                                             VERIFICATION_SCREEN_TEARING,
                                             VERIFICATION_FALSE_NEGATIVE)
from .base_dataset_staff import load_idxes_and_metas_by_langcode, lazy_image_value


blank_image = cv2.imread(path.join(path_conf.samples, "map_screen_blank.png"))

dataset = MapCalendarsDataset(lazy_load=True)

idxes_and_metas_by_langcode = load_idxes_and_metas_by_langcode(dataset)

ocrs_and_parsers_by_lang_code: dict[LanguageCode, tuple[Any, Any]] = dict()
for langcode in idxes_and_metas_by_langcode:
    language = Language.load(langcode)
    date_model = LanguageModel(model=calendar_model.date_model,
                               language=language)
    timeofday_model = LanguageModel(model=calendar_model.timeofday_model,
                                    language=language)
    symbols = "".join(set(timeofday_model.symbols + date_model.symbols))
    ocr = MapScreenCalendarOCR(langcode, symbols)
    parser = MapScreenCalendarFuzzyParser(date_model, timeofday_model)
    ocrs_and_parsers_by_lang_code[langcode] = (ocr, parser)

params = []

for langcode, idxes_and_metas in idxes_and_metas_by_langcode.items():
    ocr, parser = ocrs_and_parsers_by_lang_code[langcode]
    for idx, meta in idxes_and_metas:
        if meta.verification in (VERIFICATION_SCREEN_TEARING,
                                 VERIFICATION_FALSE_NEGATIVE):
            continue
        params.append((idx,
                       meta.date_key,
                       meta.year,
                       meta.day,
                       meta.timeofday_key,
                       lazy_image_value(dataset, idx, meta, blank_image),
                       ocr,
                       parser))


@pytest.mark.parametrize("idx,"
                         "date_key_exp,"
                         "year_exp,"
                         "day_exp,"
                         "timeofday_key_exp,"
                         "image,"
                         "ocr,"
                         "parser,",
                         params)
def test_dialog_title_dataset(idx,
                              date_key_exp,
                              year_exp,
                              day_exp,
                              timeofday_key_exp,
                              image,
                              ocr,
                              parser):
    ocr.ocr(image)  # Dry run to simulate two identical images in a row
    calendar_ocr = ocr.ocr(image)
    date_timeofday = parser.calendar(calendar_ocr)
    date_key = date_timeofday.date_key if date_timeofday is not None else None
    year = date_timeofday.year if date_timeofday is not None else None
    day = date_timeofday.day if date_timeofday is not None else None
    timeofday_key = date_timeofday.timeofday_key if date_timeofday is not None else None
    assert date_key == date_key_exp, f"OCR: {calendar_ocr}"
    assert year == year_exp, f"OCR: {calendar_ocr}"
    assert day == day_exp, f"OCR: {calendar_ocr}"
    assert timeofday_key == timeofday_key_exp, f"OCR: {calendar_ocr}"
