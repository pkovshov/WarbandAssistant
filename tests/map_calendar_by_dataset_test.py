import cv2
import numpy as np
import pytest

from wa_language.LangLoader import load_lang
from wa_datasets.MapScreen.MapCalendarDataset import MapCalendarDataset
from wa_screen_manager.MapScreen.MapScreenCalendarOCR import MapScreenCalendarOCR
from wa_screen_manager.MapScreen.MapScreenCalendarFuzzy import MapScreenCalendarFuzzy


def load_image_and_restore_crop(image_path, resolution, crop):
    width, height = resolution
    result = np.zeros((height, width, 3), dtype=np.uint8)
    image = cv2.imread(image_path)
    result[crop[1]: crop[3],
           crop[0]: crop[2]] = image
    return result


lang = load_lang()

dataset = MapCalendarDataset(lazy_load=True)

ocr = MapScreenCalendarOCR()

fuzzy = MapScreenCalendarFuzzy(lang)

idx_meta_image = []

for idx, (meta, image_path) in dataset.meta_and_image_path().items():
    image = load_image_and_restore_crop(image_path,
                                        meta.resolution,
                                        meta.crop)
    idx_meta_image.append((dataset.idx_to_stem(idx),
                           meta.date_key,
                           meta.year,
                           meta.day,
                           meta.timeofday_key,
                           image))


@pytest.mark.parametrize("idx, "                         
                         "date_key_exp, "
                         "year_exp, "
                         "day_exp, "
                         "timeofday_key_exp, "
                         "image",
                         idx_meta_image)
def test_dialog_title_dataset(idx,
                              date_key_exp,
                              year_exp,
                              day_exp,
                              timeofday_key_exp,
                              image):
    calendar_ocr = ocr.ocr(image)
    date_timeofday = fuzzy.calendar(calendar_ocr)
    date_key = date_timeofday.date_key if date_timeofday is not None else None
    year = date_timeofday.year if date_timeofday is not None else None
    day = date_timeofday.day if date_timeofday is not None else None
    timeofday_key = date_timeofday.timeofday_key if date_timeofday is not None else None
    assert date_key == date_key_exp, f"OCR: {calendar_ocr}"
    assert year == year_exp, f"OCR: {calendar_ocr}"
    assert day == day_exp, f"OCR: {calendar_ocr}"
    assert timeofday_key == timeofday_key_exp, f"OCR: {calendar_ocr}"
