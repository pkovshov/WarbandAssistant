from collections import namedtuple
import logging
import os
from os import path
import subprocess
import traceback
from typing import Dict, List, Optional, Set, Tuple

import cv2
import numpy as np
from typeguard import typechecked
import yaml


GitStatus = namedtuple("GitStatus", "branch, commit, has_modified")

# TODO: convert to a class with type checking
#       class has to support Mapping type
DatasetItem = namedtuple("DatasetItem",
                         "verified, "
                         "resolution, "
                         "language, "
                         "playername, "
                         "crop, "
                         "title_ocr, "
                         "fuzzy_score, "
                         "keys, "                         
                         "git_branch, "
                         "git_commit, "
                         "git_has_modified")

DatasetKey = namedtuple("DatasetKey",
                        "crop, "
                        "title_ocr")


class DialogScreenDataset:
    """Class that collects data for dialog screen datasets"""
    @typechecked
    def __init__(self):
        # create logger
        self.__logger = logging.getLogger(__name__)
        # process configs
        from . import dialog_screen_dataset_config
        import config
        self.__dir_path = dialog_screen_dataset_config.dataset_dir_path
        self.__resolution = config.resolution
        self.__language = config.language
        self.__playername = config.playermane
        # build crop slice and store title box and crop slice
        title_box = dialog_screen_dataset_config.title_box
        self.__title_box = title_box
        self.__title_crop_slice = (slice(title_box.t, title_box.b),
                                   slice(title_box.l, title_box.r))
        # obtain, check and store git status
        git_status = self._git_status()
        self.__git_status = git_status
        self.__logger.info(f"git status: {'HAS' if git_status.has_modified else 'NO'} modified, "
                           f"branch:{git_status.branch}, "
                           f"commit:{git_status.commit}")
        if git_status.has_modified:
            self.__logger.warning("git repository has modified files")
        # load dataset
        self.__maxidx, dataset = self._load_dataset(self.__dir_path)
        self.__dataset_keys = set(DatasetKey(crop=tuple(item.crop),
                                             title_ocr=item.title_ocr)
                                  for item in dataset)

    @typechecked
    def process(self, img: np.ndarray, title_ocr: str, title_fuzzy_score: Optional[float], title_keys: Tuple[str, ...]):
        assert img.dtype == np.uint8
        assert img.ndim == 3
        assert img.shape[0] == self.__resolution.height
        assert img.shape[1] == self.__resolution.width
        assert img.shape[2] == 3

        # check uniq dataset key
        detaset_key = DatasetKey(crop=self.__title_box,
                                 title_ocr=title_ocr)
        if detaset_key in self.__dataset_keys:
            return
        # build idx and file pathes
        idx = self.__maxidx + 1
        idx_str = f"{idx:06d}"
        yaml_file_path = path.join(self.__dir_path, idx_str + ".yaml")
        png_file_path = path.join(self.__dir_path, idx_str + ".png")
        # build crop img
        crop_img = img[self.__title_crop_slice]
        # build dataset item
        item = DatasetItem(verified=False,
                           resolution=tuple(self.__resolution),
                           language=self.__language,
                           playername=self.__playername,
                           crop=tuple(self.__title_box),
                           title_ocr=title_ocr,
                           fuzzy_score=title_fuzzy_score,
                           keys=title_keys,
                           git_branch=self.__git_status.branch,
                           git_commit=self.__git_status.commit,
                           git_has_modified=self.__git_status.has_modified)
        try:
            try:
                if path.isfile(yaml_file_path):
                    self.__logger.warning("rewrite existent file: " + yaml_file_path)
                with open(yaml_file_path, "w") as file:
                    data = item._asdict()
                    yaml.safe_dump(data, file, default_flow_style=False)
            except Exception as error:
                self.__logger.warning("error on writing item data to file, "
                                      f"idx:{idx_str}, "
                                      f"title_ocr:{repr(title_ocr)}\n" +
                                      traceback.format_exc())
                raise error
            try:
                if path.isfile(png_file_path):
                    self.__logger.warning("rewrite existent file: " + png_file_path)
                cv2.imwrite(png_file_path, crop_img)
            except Exception as error:
                self.__logger.warning("error on writing cropped image to file, "
                                      f"idx:{idx_str}, "
                                      f"title_ocr:{repr(title_ocr)}\n" +
                                      traceback.format_exc())
                self.__logger.warning("cannot write item to " + png_file_path)
                raise error
        except Exception:
            pass
        else:
            self.__maxidx = idx
            self.__dataset_keys.add(detaset_key)

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

    @typechecked
    def _load_dataset(self, dir_path: str) -> Tuple[int, List[DatasetItem]]:
        if not path.isdir(dir_path):
            self.__logger.warning("path is not a directory: " + dir_path)
            return 0, []
        # initiate yaml and png str indexes
        yaml_idx_to_name: Dict[int, str] = dict()
        png_idx_to_name: Dict[int, str] = dict()
        # collect yaml and png indexes
        file_names = os.listdir(dir_path)
        for file_name in file_names:
            # check that we are working with a file
            if not os.path.isfile(path.join(dir_path, file_name)):
                self.__logger.warning("discard not a file: " + file_name)
                continue
            # check file name format is 000001.png or 000001.yaml
            # extract extension and numeric index
            split = file_name.split(".")
            if len(split) != 2:
                self.__logger.warning("discard incorrect file name: " + file_name)
                continue
            idx_str, ext = split
            if len(idx_str) < 6:
                self.__logger.warning("discard incorrect file name: " + file_name)
                continue
            if len(idx_str) > 6 and idx_str[0]=="0":
                self.__logger.warning("discard incorrect file name: " + file_name)
                continue
            try:
                idx = int(idx_str)
            except ValueError:
                self.__logger.warning("discard incorrect file name: " + file_name)
                continue
            # append index to yaml or png list
            if ext == "yaml":
                yaml_idx_to_name[idx] = file_name
            elif ext == "png":
                png_idx_to_name[idx] = file_name
            else:
                self.__logger.warning("discard incorrect file name: " + file_name)
                continue
        # check that yaml files exist for all the png files
        lone_png_idx_set = png_idx_to_name.keys() - yaml_idx_to_name.keys()
        for idx in lone_png_idx_set:
            self.__logger.warning("discard png without yaml: " + png_idx_to_name[idx])
        # check that png files exist for all the yaml files
        # decline lone yaml files
        lone_yaml_idx_set = yaml_idx_to_name.keys() - png_idx_to_name.keys()
        for idx in lone_yaml_idx_set:
            self.__logger.warning("discard yaml without png: " + yaml_idx_to_name[idx])
            del yaml_idx_to_name[idx]
        # build items list
        items: List[DatasetItem] = []
        for file_name in yaml_idx_to_name.values():
            # TODO: process PermissionError
            with open(path.join(dir_path, file_name)) as file:
                # TODO: process YAMLError
                data = yaml.safe_load(file)
                # TODO: process TypeError, ValueError, AttributeError
                item = DatasetItem(**data)
                items.append(item)
        # find last index
        max_idx = max(yaml_idx_to_name.keys()) if len(yaml_idx_to_name) > 0 else 0
        # build and return result
        return max_idx, items
