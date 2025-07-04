import logging
import subprocess
from typing import Optional, Tuple

import numpy as np
from typeguard import typechecked

from wa_datasets.DialogScreen.DialogTitleDataset import DialogTitleDataset
from wa_datasets.DialogScreen.DialogRelationDataset import DialogRelationDataset


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
    def process(self,
                image: np.ndarray,
                screen_sample_matches: bool,
                title_ocr: str,
                title: str,
                title_fuzzy_score: Optional[float],
                title_keys: Tuple[str, ...],
                relation_ocr: Optional[str],
                relation: Optional[int]):
        if not screen_sample_matches and len(title_keys) == 0:
            return
        self.__dialog_title_dataset.add(screenshot=image,
                                        sample_matches=screen_sample_matches,
                                        title_ocr=title_ocr,
                                        title_fuzzy_score=title_fuzzy_score,
                                        title_keys=title_keys)
        if relation_ocr is not None:
            self.__dialog_relation_dataset.add(screenshot=image,
                                               screen_sample_matches=screen_sample_matches,
                                               relation_ocr=relation_ocr,
                                               relation=relation)
