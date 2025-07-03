import logging
import os
import re
from types import MappingProxyType
from typing import Mapping, List

from typeguard import typechecked

from .LangValParser import Interpolation


logger = logging.getLogger(__name__)


class LangValue(Interpolation):
    @typechecked
    def __new__(cls, src: str, file: str, raw: bool = False):
        """
        :param file: A file path the value is loaded from.
        """
        obj = super().__new__(cls, src, raw)
        obj.__file = file
        return obj

    @property
    def file(self):
        return self.__file


@typechecked
def load_lang() -> Mapping[str, LangValue]:
    import path_conf
    lang_dir_path = path_conf.language
    lang_file_paths = find_csv(lang_dir_path)
    if len(lang_file_paths) == 0:
        raise ValueError(f"No csv files found at {lang_dir_path}")
    lang = load_files(*lang_file_paths)
    if len(lang) == 0:
        raise ValueError(f"Empty lang is loaded by {lang_dir_path}")
    return lang


@typechecked
def load_files(*args: str, encoding=None) -> Mapping[str, LangValue]:
    lang = {}
    dup_keys = set()
    for file_path in args:
        with open(file_path, encoding=encoding) as file:
            for number, line in enumerate(file, start=1):
                line = line[:-1]
                pos = line.find("|")
                if pos < 0:
                    logger.warning(f"{file_path}:{number} Absent splitter. Discard line: {line}")
                    continue
                key, val = line[:pos], line[pos + 1:]
                if key == "":
                    logger.warning(f"{file_path}:{number} Empty key. Discard line: {line}")
                    continue
                if key in lang:
                    description = f"{file_path}:{number} Not unique key. Discard line"
                    if key not in dup_keys:
                        prev_val = lang[key]
                        logger.warning(f"{prev_val.file} Duplicated key".ljust(len(description)) + f": {key}|{prev_val}")
                        dup_keys.add(key)
                    logger.warning(description + f": {line}")
                    continue
                try:
                    lang_val = LangValue(val, file_path)
                except ValueError as error:
                    logger.warning(f"{file_path}:{number} Parser error. Use raw mode with value: '{line}' Error: {error}")
                    lang_val = LangValue(val, file_path, raw=True)
                lang[key] = lang_val
    return MappingProxyType(lang)


def find_csv(*args: str) -> List[str]:
    file_pathes = []
    for dir_path in args:
        for file_name in os.listdir(dir_path):
            if re.fullmatch(r'.*\.csv', file_name):
                file_path = os.path.join(dir_path, file_name)
                if os.path.isfile(file_path):
                    file_path = os.path.abspath(file_path)
                    file_pathes.append(file_path)
    return file_pathes


__all__ = ["load_files", "find_csv"]


if __name__ == "__main__":
    import traceback
    import sys

    # this prevents logs buffering in PyCharm
    sys.stderr = sys.stdout

    for dir_path in ("/aaaweaewra",
                     "test",
                     "test/test_file_1",
                     "test/test_file_2",
                     "test/test_file_3",
                     "test/test_file_4"):
        print(f"load dir('{dir_path}')", flush=True)
        lang = {}
        try:
            lang = load_files(*find_csv(dir_path))
        except Exception as e:
            print(traceback.format_exc(), flush=True)
        for key, val in lang.items():
            file = os.path.basename(val.file)
            print(f"{file}: {key}|{val}")
        print()

    LANG_EN_PATH = "/sandbox/MountAndBladeWarband/resources/languages/en/"
    print(f"load dir {LANG_EN_PATH}")
    file_pathes = find_csv(LANG_EN_PATH)
    lang = load_files(*file_pathes)
    print()

    for key, val in list(lang.items())[::500]:
        file = os.path.basename(val.file)
        print(f"{file}: {key}|{val}")
    print()

    for file_path in file_pathes:
        prefix_set = set(key.split("_")[0] for key, val in lang.items() if val.file == file_path)
        print(os.path.basename(file_path), ", ".join(prefix_set), sep=": ")

    print()
    
    key = "skl_trainer_desc"
    print(key, lang[key], sep="|")

    key = "ui_chest"
    print(key, lang[key], sep="|")
