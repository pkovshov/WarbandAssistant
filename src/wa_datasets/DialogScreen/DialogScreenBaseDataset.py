from abc import ABC, abstractmethod
from collections import namedtuple
from collections.abc import Hashable
from enum import Enum
import logging
import os
from os import path
import traceback
from types import MappingProxyType
from typing import Dict, Mapping, NamedTuple, Optional, Set, Tuple

import cv2
import numpy as np
from typeguard import typechecked
import yaml


class State(Enum):
    INIT = "INIT"
    BLOCKED = "BLOCKED"
    META_LOADED = "META_LOADED"


class Resolution(NamedTuple):
    """WITH, HEIGHT"""
    width: int  # width
    height: int  # height


MetaAndImagePath = namedtuple("MetaAndImage",
                              "meta, "
                              "image_path")


class DialogScreenBaseDataset(ABC):
    @typechecked
    def __init__(self,
                 dataset_dir_name: str,
                 new_screenshots_resolution: Optional[Resolution],
                 lazy_load: bool = False):
        import path_conf
        self.__logger = logging.getLogger(__name__)
        self.__name = dataset_dir_name
        self.__dir_path = path.join(path_conf.datasets,
                                    dataset_dir_name)
        self.__resolution = new_screenshots_resolution
        self.__state = State.INIT
        self.__max_idx = 0
        if not lazy_load:
            self.__load()

    @typechecked
    def meta_and_image_path(self) -> Optional[dict[int, MetaAndImagePath[object, str]]]:
        self.__load()
        if self.__state is State.BLOCKED:
            self.__logger.warning(f"BLOCKED {self.__name} dataset does not support meta_and_image")
            return None
        result = dict()
        for idx, meta in self.__meta.items():
            result[idx] = MetaAndImagePath(meta=meta,
                                           image_path=path.join(self.__dir_path,
                                                                self.__idx_to_png(idx)))
        return result

    @typechecked
    def add(self, meta: object, screenshot: np.ndarray):
        self.__load()
        if self.__state is State.BLOCKED:
            self.__logger.warning(f"BLOCKED {self.__name} dataset does not support add")
            return
        assert screenshot.dtype == np.uint8
        assert screenshot.ndim == 3
        if self.__resolution:
            assert screenshot.shape[0] == self.__resolution.height
            assert screenshot.shape[1] == self.__resolution.width
        assert screenshot.shape[2] == 3
        meta_key = self._meta_to_key(meta)
        if meta_key in self.__meta_index:
            return
        data = self._meta_to_data(meta)
        image = self._preprocess(screenshot)
        idx = self.__max_idx + 1
        if not self.__write_data(idx, data):
            self.__logger.warning(f"meta causes above error: {repr(meta)}")
            return
        if not self.__write_image(idx, image):
            self.__logger.warning(f"meta causes above error: {repr(meta)}")
            return
        self.__max_idx = idx
        self.__meta_index.add(meta_key)

    @typechecked
    def replace_meta(self, idx: int, meta: object):
        self.__load()
        if self.__state is State.BLOCKED:
            self.__logger.warning(f"BLOCKED {self.__name} dataset does not support replace_meta")
            return
        if idx not in self.__meta:
            self.__logger.warning(f"DISCARD replacing unknown index {idx}")
            return
        meta_key = self._meta_to_key(meta)
        if not isinstance(meta_key, Hashable):
            self.__logger.warning(f"DISCARD replacing on meta with non-hashable meta key {repr(meta)}")
            return
        if (hash(meta_key) != hash(self._meta_to_key(self.__meta[idx])) and
            meta_key in self.__meta_index):
            self.__logger.warning(f"DISCARD replacing on non-uniq meta {repr(meta)}")
            return
        data = self._meta_to_data(meta)
        if not self.__write_data(idx, data):
            self.__logger.warning(f"meta causes above error: {repr(meta)}")
            self.__logger.warning(f"DISCARD replacing due to write error")
            return
        self.__meta[idx] = meta

    @typechecked
    def idx_to_stem(self, idx: int) -> str:
        return f"{idx:06d}"

    @abstractmethod
    def _meta_to_data(self, data: object) -> dict:
        """Convert dataset-specific metadata to a dictionary for YAML storage."""
        raise NotImplemented

    @abstractmethod
    def _data_to_meta(self, data: dict) -> object:
        """Create a dataset-specific metadata from loaded data dictionary."""
        raise NotImplemented

    @abstractmethod
    def _meta_to_key(self, meta: object) -> Optional[Hashable]:
        """Create a dataset specific key from dataset specific meta.

        Meta key is uniq for meta items within dataset
        Return None to exclude passed meta from meta key index"""
        raise NotImplemented

    @abstractmethod
    def _preprocess(self, screenshot: np.ndarray) -> np.ndarray:
        """Preprocess the screenshot before saving it to a file."""
        raise NotImplemented

    @typechecked
    def __write_data(self, idx: int, data: dict) -> bool:
        yaml_file_path = path.join(self.__dir_path,
                                   self.__idx_to_yaml(idx))
        if path.isfile(yaml_file_path):
            self.__logger.warning(f"REWRITE existent yaml file {yaml_file_path}")
        try:
            with open(yaml_file_path, "w") as file:
                yaml.safe_dump(data, file, default_flow_style=False)
        except Exception:
            self.__logger.warning(f"ERROR ON WRITING meta to file {yaml_file_path}\n" +
                                  traceback.format_exc())
            return False
        return True

    @typechecked
    def __write_image(self, idx: int, image: np.ndarray) -> bool:
        png_file_path = path.join(self.__dir_path,
                                  self.__idx_to_png(idx))
        if path.isfile(png_file_path):
            self.__logger.warning(f"REWRITE existent png file {png_file_path}")
        try:
            cv2.imwrite(png_file_path, image)
        except Exception:
            self.__logger.warning(f"ERROR ON WRITING image to file {png_file_path}\n" +
                                  traceback.format_exc())
            return False
        return True

    @typechecked
    def __idx_to_yaml(self, idx: int) -> str:
        return self.idx_to_stem(idx) + "." + "yaml"

    @typechecked
    def __idx_to_png(self, idx: int) -> str:
        return self.idx_to_stem(idx) + "." + "png"

    @typechecked
    def __file_name_to_idx_and_ext(self, file_name: str) -> Optional[Tuple[int, str]]:
        # check file format
        split = file_name.split(".")
        if len(split) != 2:
            return None
        stem, ext = split
        # check that stem is a number
        try:
            idx = int(stem)
        except ValueError:
            return None
        # check that the idx maps to the stem of a loaded file
        if self.idx_to_stem(idx) != stem:
            return None
        return idx, ext

    @typechecked
    def __load_indexes(self) -> Optional[Set[int]]:
        if not path.isdir(self.__dir_path):
            self.__logger.warning(f"BLOCK {self.__name} dataset. Not a directory {self.__dir_path}")
            self.__state = State.BLOCKED
            return None
        # collect yaml and png indexes
        yaml_idx_set = set()
        png_idx_set = set()
        for file_name in os.listdir(self.__dir_path):
            # check that we are working with a file
            file_path = path.join(self.__dir_path, file_name)
            if not os.path.isfile(file_path):
                self.__logger.warning(f"DISCARD {file_name}. Not a file {file_path}")
                continue
            # got index and extension
            idx_and_ext = self.__file_name_to_idx_and_ext(file_name)
            if idx_and_ext is None:
                self.__logger.warning(f"DISCARD {file_name}. Incorrect file name format")
                continue
            idx, ext = idx_and_ext
            # check the extension and append index to corresponding set
            if ext == "yaml":
                yaml_idx_set.add(idx)
            elif ext == "png":
                png_idx_set.add(idx)
            else:
                self.__logger.warning(f"DISCARD {file_name}. Incorrect extension")
                continue
        # check that yaml files exist for all the png files
        lone_png_idx_set = png_idx_set - yaml_idx_set
        for idx in lone_png_idx_set:
            self.__logger.warning(f"DISCARD {self.__idx_to_png(idx)}. Absent yaml file")
        # check that png files exist for all the yaml files
        # decline lone yaml files
        lone_yaml_idx_set = yaml_idx_set - png_idx_set
        for idx in lone_yaml_idx_set:
            self.__logger.warning(f"DISCARD {self.__idx_to_yaml(idx)}. Absent png file")
            yaml_idx_set.remove(idx)
        # calculate max index
        self.__max_idx = max(yaml_idx_set) if len(yaml_idx_set) > 0 else 0
        # result
        return yaml_idx_set

    @typechecked
    def __load_data(self) -> Optional[Dict[int, dict]]:
        idx_set = self.__load_indexes()
        if idx_set is None:
            return None
        idx_to_data = {}
        for idx in sorted(idx_set):
            yaml_file_path = path.join(self.__dir_path,
                                       self.__idx_to_yaml(idx))
            # load data from yaml file
            try:
                with open(yaml_file_path) as file:
                    data = yaml.safe_load(file)
            except PermissionError:
                self.__logger.warning(f"PERMISSION DENIED to read file {self.__idx_to_yaml(idx)}")
            except FileNotFoundError:
                self.__logger.warning(f"FILE NOT FOUND {self.__idx_to_yaml(idx)}")
            except yaml.YAMLError as error:
                self.__logger.warning(f"FAILED TO PARSE yaml {self.__idx_to_yaml(idx)}\n"
                                      f"{type(error).__name__}('{error}'): \n" +
                                      traceback.format_exc())
            else:
                idx_to_data[idx] = data
        return idx_to_data

    def __load(self):
        if self.__state is not State.INIT:
            return
        idx_to_data = self.__load_data()
        if idx_to_data is None:
            return
        # all the meta in the dataset
        self.__meta = dict()
        # all the meta keys in the dataset
        self.__meta_index = set()
        for idx in sorted(idx_to_data):
            try:
                meta = self._data_to_meta(idx_to_data[idx])
            except Exception as error:
                self.__logger.warning(f"FAILED TO PARSE as meta {self.__idx_to_yaml(idx)}\n"
                                      f"{type(error).__name__}('{error}'): \n" +
                                      traceback.format_exc())
                continue
            meta_key = self._meta_to_key(meta)
            assert isinstance(meta_key, Hashable)
            if meta_key in self.__meta_index:
                self.__logger.warning(f"DISCARD {self.__idx_to_yaml(idx)}. Non-uniq content")
                continue
            self.__meta_index.add(meta_key)
            self.__meta[idx] = meta
        self.__state = State.META_LOADED
