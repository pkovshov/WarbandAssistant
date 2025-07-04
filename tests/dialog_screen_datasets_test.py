import shutil
import os
from os import path

import numpy as np

import path_conf
from wa_types import Box, Resolution
from wa_datasets.DialogScreen.DialogTitleDataset import DialogTitleDataset

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
for dataset in [DialogTitleDataset.NAME]:
    src_path = path.join(path_conf.datasets, dataset)
    dst_path = path.join(path_conf.test_output, dataset)
    shutil.copytree(src_path, dst_path)

# Override the datasets path for testing in a controlled environment
path_conf.datasets = path_conf.test_output

def test_dialog_title_dataset():
    dialog_title_dataset_path = path.join(path_conf.datasets,
                                          DialogTitleDataset.NAME)
    files_count_before = len(os.listdir(dialog_title_dataset_path))
    width, height = 400, 200
    dataset = DialogTitleDataset(resolution=Resolution(width, height),
                                 crop=Box(0, 0, 50, 50),
                                 language="en",
                                 playername="John Doe")
    screenshot = np.zeros((height, width, 3), dtype=np.uint8)
    dataset.add(screenshot=screenshot,
                sample_matches=True,
                title_ocr="Marry Wong",
                title_fuzzy_score=None,
                title_keys=())
    files_count_after = len(os.listdir(dialog_title_dataset_path))
    assert files_count_after == files_count_before + 2
