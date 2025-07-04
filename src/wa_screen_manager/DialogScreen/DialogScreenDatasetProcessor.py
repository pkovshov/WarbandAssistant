import logging
import subprocess
from typing import Optional, Tuple

import numpy as np
from typeguard import typechecked

from wa_datasets.DialogScreen.DialogTitleDataset import DialogTitleDataset


class DialogScreenDatasetProcessor:
    """Class that collects data for dialog screen datasets"""
    @typechecked
    def __init__(self, playername: Optional[str]):
        from . import dialog_screen_config
        from wa_screen_manager import config
        self.__logger = logging.getLogger(__name__)
        self.__dataset = DialogTitleDataset(resolution=config.resolution,
                                            crop=dialog_screen_config.title_box,
                                            language=config.language,
                                            playername=playername)

    @typechecked
    def process(self,
                image: np.ndarray,
                dialog_sample_matches: bool,
                title_ocr: str,
                title_fuzzy_score: Optional[float],
                title_keys: Tuple[str, ...]):
        if not dialog_sample_matches and len(title_keys) == 0:
            return
        self.__dataset.add(screenshot=image,
                           sample_matches=dialog_sample_matches,
                           title_ocr=title_ocr,
                           title_fuzzy_score=title_fuzzy_score,
                           title_keys=title_keys)
