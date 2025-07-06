import logging
import subprocess
from typing import Optional, Tuple

import numpy as np
from typeguard import typechecked

from wa_datasets.DialogScreen.DialogTitleDataset import DialogTitleDataset
from wa_datasets.DialogScreen.DialogRelationDataset import DialogRelationDataset
from .DialogScreenEvent import DialogScreenEvent


class DialogScreenDatasetProcessor:
    """Class that collects data for dialog screen datasets"""
    @typechecked
    def __init__(self, playername: Optional[str]):
        from . import dialog_screen_config
        from wa_screen_manager import config
        self.__logger = logging.getLogger(__name__)
        self.__dialog_title_dataset = DialogTitleDataset(resolution=config.resolution,
                                                         crop=dialog_screen_config.title_box,
                                                         language=config.language,
                                                         playername=playername)
        self.__dialog_relation_dataset = DialogRelationDataset(resolution=config.resolution,
                                                               crop=dialog_screen_config.relation_box,
                                                               language=config.language)

    @typechecked
    def process(self, event: DialogScreenEvent):
        self.__dialog_title_dataset.add(screenshot=event.image,
                                        sample_matches=True,
                                        title_ocr=event.title_ocr,
                                        title_fuzzy_score=event.title_fuzzy_score,
                                        title_keys=event.title_keys)
        if event.relation_ocr is not None:
            self.__dialog_relation_dataset.add(screenshot=event.image,
                                               screen_sample_matches=True,
                                               relation_ocr=event.relation_ocr,
                                               relation=event.relation)
