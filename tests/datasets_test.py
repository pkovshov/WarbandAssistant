import shutil
import os
from os import path

import numpy as np

import path_conf
from wa_types import Box, Resolution
from wa_language.Language import RootLanguage
from wa_language.LangKey import LangKey
from wa_language.LangVar import LangVar, PlayerSex, PlayerSexVar, PLAYER_NAME_VAR
from wa_datasets.DialogBodiesDataset import DialogBodiesDataset
from wa_datasets.DialogTitlesDataset import DialogTitlesDataset
from wa_datasets.DialogRelationsDataset import DialogRelationsDataset
from wa_datasets.MapCalendarsDataset import MapCalendarsDataset

# Create the output directory if it doesn't exist
os.makedirs(path_conf.test_output, exist_ok=True)

# Clear the contents of test_output
for item in os.listdir(path_conf.test_output):
    item_path = path.join(path_conf.test_output, item)
    if path.isdir(item_path):
        shutil.rmtree(item_path)
    else:
        os.remove(item_path)

# Copy the dialog screen datasets to test_output
for dataset in [DialogBodiesDataset.NAME,
                DialogTitlesDataset.NAME,
                DialogRelationsDataset.NAME,
                MapCalendarsDataset.NAME]:
    src_path = path.join(path_conf.datasets, dataset)
    dst_path = path.join(path_conf.test_output, dataset)
    shutil.copytree(src_path, dst_path)

# Override the datasets path for testing in a controlled environment
path_conf.datasets = path_conf.test_output


def test_dialog_bodies_dataset():
    import path_conf
    from wa_screen_manager.DialogScreen import dialog_screen_config
    dialog_bodies_dataset_path = path.join(path_conf.datasets,
                                           DialogBodiesDataset.NAME)
    files_count_before = len(os.listdir(dialog_bodies_dataset_path))
    lang = RootLanguage(
        {"kl_marry": "Marry",
         "kl_wong": "Wong",
         "kl_marry_wong": "Marry Wong",
         "kl_meir_wong": "Marry Wong",
         "kl_complex": "Hi, {sir/lady} {playername}. My name is {reg1}"}
    )
    width, height = 400, 200
    dataset = DialogBodiesDataset(resolution=Resolution(width, height),
                                  crop=Box(0, 0, 50, 50),
                                  language="en",
                                  player_name="John Doe",
                                  player_sex=PlayerSex.MALE,
                                  blank_img_path=path.join(path_conf.samples,
                                                           dialog_screen_config.dialog_screen_blank_img_path)
                                  )
    screenshot = np.zeros((height, width, 3), dtype=np.uint8)
    dataset.add(screenshot=screenshot,
                screen_sample_matches=True,
                title_keys=(LangKey("kl_marry"), LangKey("kl_wong")),
                body_ocr="Marry Wong",
                body_bounds=(lang["kl_marry_wong"], lang["kl_meir_wong"]))
    files_count_after = len(os.listdir(dialog_bodies_dataset_path))
    assert files_count_after == files_count_before + 2
    files_count_before = files_count_after
    dataset.add(screenshot=screenshot,
                screen_sample_matches=True,
                title_keys=(LangKey("kl_marry"), LangKey("kl_wong")),
                body_ocr="Hi sir Goracio. My name is Vlan",
                body_bounds=((lang["kl_complex"].bind(PlayerSexVar, PlayerSex.MALE)
                                                .bind(PLAYER_NAME_VAR, "Horatio")
                                                .bind(LangVar("reg1"), "Vlan"),)
                            )
                )


def test_dialog_titles_dataset():
    dialog_title_dataset_path = path.join(path_conf.datasets,
                                          DialogTitlesDataset.NAME)
    files_count_before = len(os.listdir(dialog_title_dataset_path))
    width, height = 400, 200
    dataset = DialogTitlesDataset(resolution=Resolution(width, height),
                                  crop=Box(0, 0, 50, 50),
                                  language="en",
                                  player_name="John Doe")
    screenshot = np.zeros((height, width, 3), dtype=np.uint8)
    dataset.add(screenshot=screenshot,
                screen_sample_matches=True,
                title_ocr="Marry Wong",
                title_fuzzy_score=None,
                title_keys=(LangKey("kl_marry"), LangKey("kl_wong")))
    files_count_after = len(os.listdir(dialog_title_dataset_path))
    assert files_count_after == files_count_before + 2


def test_dialog_relations_dataset():
    dialog_relation_dataset_path = path.join(path_conf.datasets,
                                             DialogRelationsDataset.NAME)
    files_count_before = len(os.listdir(dialog_relation_dataset_path))
    width, height = 400, 200
    dataset = DialogRelationsDataset(resolution=Resolution(width, height),
                                    crop=Box(0, 0, 50, 50),
                                    language="en")
    screenshot = np.zeros((height, width, 3), dtype=np.uint8)
    dataset.add(screenshot=screenshot,
                screen_sample_matches=True,
                relation_ocr="16",
                relation=16)
    files_count_after = len(os.listdir(dialog_relation_dataset_path))
    assert files_count_after == files_count_before + 2


def test_map_calendars_dataset():
    map_calendar_dataset_path = path.join(path_conf.datasets,
                                          MapCalendarsDataset.NAME)
    files_count_before = len(os.listdir(map_calendar_dataset_path))
    width, height = 400, 200
    dataset = MapCalendarsDataset(resolution=Resolution(width, height),
                                 crop=Box(0, 0, 50, 50),
                                 language="en")
    screenshot = np.zeros((height, width, 3), dtype=np.uint8)
    dataset.add(screenshot=screenshot,
                calendar_ocr="date\ntime",
                calendar_overlapped=False,
                date_key=LangKey("da_key_jan"),
                year=1278,
                day=20,
                timeofday_key=LangKey("da_key_dawn"))
    files_count_after = len(os.listdir(map_calendar_dataset_path))
    assert files_count_after == files_count_before + 2


def test_map_calendars_dataset_meta_keys():
    map_calendar_dataset_path = path.join(path_conf.datasets,
                                          MapCalendarsDataset.NAME)
    files_count_before = len(os.listdir(map_calendar_dataset_path))
    width, height = 400, 200
    dataset = MapCalendarsDataset(resolution=Resolution(width, height),
                                 crop=Box(0, 0, 50, 50),
                                 language="en")
    # add two false-negative items with same calendar_ocr but different images
    screenshot = np.zeros((height, width, 3), dtype=np.uint8)
    dataset.add(screenshot=screenshot,
                calendar_ocr="wrong_ocr",
                calendar_overlapped=True,
                date_key=None,
                year=None,
                day=None,
                timeofday_key=None)
    screenshot = np.ones((height, width, 3), dtype=np.uint8)
    dataset.add(screenshot=screenshot,
                calendar_ocr="wrong_ocr",
                calendar_overlapped=True,
                date_key=None,
                year=None,
                day=None,
                timeofday_key=None)
    files_count_after = len(os.listdir(map_calendar_dataset_path))
    assert files_count_after == files_count_before + 2
    # try to add one more false-negative item with non-uniq calendar_ocr and non-uniq images
    files_count_before = files_count_after
    screenshot = np.ones((height, width, 3), dtype=np.uint8)
    dataset.add(screenshot=screenshot,
                calendar_ocr="wrong_ocr",
                calendar_overlapped=True,
                date_key=None,
                year=None,
                day=None,
                timeofday_key=None)
    files_count_after = len(os.listdir(map_calendar_dataset_path))
    assert files_count_after == files_count_before
