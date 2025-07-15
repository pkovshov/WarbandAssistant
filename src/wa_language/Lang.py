from typing import Mapping

from typeguard import typechecked

from . import loader
from .loader import LangValue


@typechecked
def load() -> Mapping[str, LangValue]:
    import path_conf
    lang_dir_path = path_conf.language
    lang_file_paths = loader.find_csv(lang_dir_path)
    if len(lang_file_paths) == 0:
        raise ValueError(f"No csv files found at {lang_dir_path}")
    lang = loader.load_files(*lang_file_paths)
    if len(lang) == 0:
        raise ValueError(f"Empty lang is loaded by {lang_dir_path}")
    return lang