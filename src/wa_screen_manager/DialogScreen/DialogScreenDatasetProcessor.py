import logging
import subprocess
from typing import Optional, Tuple

import numpy as np
from typeguard import typechecked
from wa_types import Resolution
from wa_datasets.DialogScreen.DialogTitleDataset import (DialogTitleDataset,
                                                         GitStatus)

from .DialogScreenArtifactsProcessor import DialogScreenArtifactsProcessor


class DialogScreenDatasetProcessor(DialogScreenArtifactsProcessor):
    """Class that collects data for dialog screen datasets"""
    @typechecked
    def __init__(self, playername: Optional[str]):
        from . import dialog_screen_config
        from wa_screen_manager import config
        self.__logger = logging.getLogger(__name__)
        git_status = self._git_status()
        self.__logger.info(f"git status: {'HAS' if git_status.has_modified else 'NO'} modified, "
                           f"branch:{git_status.branch}, "
                           f"commit:{git_status.commit}")
        if git_status.has_modified:
            self.__logger.warning("git repository has modified files")
        self.__dataset = DialogTitleDataset(resolution=config.resolution,
                                            crop=dialog_screen_config.title_box,
                                            language=config.language,
                                            playername=playername,
                                            git_status=git_status)

    @typechecked
    def process(self,
                img: np.ndarray,
                sample_matches: bool,
                title_ocr: str,
                title_fuzzy_score: Optional[float],
                title_keys: Tuple[str, ...]):
        if not sample_matches and len(title_keys) == 0:
            return
        self.__dataset.add(screenshot=img,
                           sample_matches=sample_matches,
                           title_ocr=title_ocr,
                           title_fuzzy_score=title_fuzzy_score,
                           title_keys=title_keys)

    @typechecked
    def _git_status(self) -> GitStatus:
        # TODO: check and process a case when
        #       working directory is out of project git repo
        # get current branch
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True
        ).strip()
        # get current commit
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True
        ).strip()
        # check for modified files in the working tree and/or staging area
        has_modified = False
        status_lines = subprocess.check_output(
            ["git", "status", "--porcelain"],
            text=True
        ).splitlines()
        for line in status_lines:
            staged = line[0]
            working_tree = line[1]
            if 'M' in (staged, working_tree):
                has_modified = True
                break
        # build and return GitStatus
        return GitStatus(branch=branch, commit=commit, has_modified=has_modified)
