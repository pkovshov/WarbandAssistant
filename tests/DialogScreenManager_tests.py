from os import path

import cv2
import numpy as np
from typeguard import TypeCheckError

from wa_types import Box, Resolution
from wa_language import Lang
from wa_screen_manager.DialogScreen.DialogScreenManager import DialogScreenManager
from wa_screen_manager.DialogScreen.DialogScreenEvent import DialogScreenEvent
from wa_datasets.DialogScreen.DialogTitleDataset import DialogTitleDataset, VERIFICATION_NOT_A_DIALOG_TITLE
from wa_datasets.DialogScreen.DialogRelationDataset import DialogRelationDataset
from path_conf import samples as samples_dir_path

lang = Lang.load()

dialog_titles_dataset = DialogTitleDataset(lazy_load=True)
dialog_relations_dataset = DialogRelationDataset(lazy_load=True)

dialog_blank_image_path = path.join(samples_dir_path, "dialog_screen_blank.png")
dialog_blank_img = cv2.imread(dialog_blank_image_path)

for dialog_title_meta, dialog_title_image_path in dialog_titles_dataset.meta_and_image_path().values():
    if dialog_title_meta.verification == VERIFICATION_NOT_A_DIALOG_TITLE:
        continue
    if dialog_title_meta.sample_matches is False:
        continue
    if "wa_player" in dialog_title_meta.keys:
        continue
    break
dialog_title_image = cv2.imread(dialog_title_image_path)

resolution = Resolution(*dialog_title_meta.resolution)

dialog_relation_meta, dialog_relation_image_path = next(iter(dialog_relations_dataset.meta_and_image_path().values()))
dialog_relation_image = cv2.imread(dialog_relation_image_path)

dialog_with_title_only_image = dialog_blank_img.copy()
dialog_with_title_only_image[Box(*dialog_title_meta.crop).slice] = dialog_title_image

dialog_with_title_and_relation_image = dialog_with_title_only_image.copy()
dialog_with_title_and_relation_image[Box(*dialog_relation_meta.crop).slice] = dialog_relation_image

empty_image = np.zeros((resolution.height, resolution.width, 3), dtype=np.uint8)


def test_check_listener_signature():
    def listener1(param: int):
        print(param)
    def listener2(param1: int, param2: str):
        print(param1, param2)

    dialog_screen_manager = DialogScreenManager(lang=lang)

    # alas, no TypeCheckError is raised for such call
    dialog_screen_manager.add_event_listener(listener1)

    try:
        dialog_screen_manager.add_event_listener("not-callable")
    except TypeCheckError:
        pass
    else:
        # we wish a TypeCheckError to be raised for such call
        assert False

    try:
        dialog_screen_manager.add_event_listener(listener2)
    except TypeCheckError:
        pass
    else:
        # we wish a TypeCheckError to be raised for such call
        assert False


def test_do_not_send_two_same_events_in_a_row():
    events = []
    def listener(event: DialogScreenEvent):
        events.append(event)
    dialog_screen_manager = DialogScreenManager(lang=lang)
    dialog_screen_manager.add_event_listener(listener)
    assert len(events) == 0
    dialog_screen_manager.process(dialog_with_title_only_image)
    assert len(events) == 1
    dialog_screen_manager.process(dialog_with_title_only_image)
    assert len(events) == 1
    dialog_screen_manager.process(dialog_with_title_only_image)
    assert len(events) == 1
    dialog_screen_manager.process(dialog_with_title_and_relation_image)
    assert len(events) == 2
    dialog_screen_manager.process(empty_image)
    assert len(events) == 2
    dialog_screen_manager.process(dialog_with_title_and_relation_image)
    assert len(events) == 3
    dialog_screen_manager.process(dialog_with_title_and_relation_image)
    assert len(events) == 3
