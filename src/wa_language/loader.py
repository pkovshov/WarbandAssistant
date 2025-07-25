import logging
import os
import re
from typing import Dict, List, Optional

from wa_typechecker import typechecked


logger = logging.getLogger(__name__)


@typechecked
def load_files(*args: str, special_language: Optional[Dict[str, str]] = None, encoding=None, ) -> Dict[str, str]:
    """
    :param args: Paths to the files to be loaded.
    :param special_language: An additional language that is not present in the files or uses special keys.
    :param encoding: Encoding value passed to the built-in 'open' function.
    :return: A dictionary loaded from the files and optionally extended with the additional language if provided.
    """
    language = special_language.copy() if special_language else {}
    source = ({key: "special_language:" for key in special_language}
              if special_language
              else {})
    if '' in language:
        logger.warning(f"special_language: Empty key. Discard line: |{language['']}")
        del language['']
    dup_keys = set()
    source_str = lambda file_path, number: f"{file_path}:{number}"
    for file_path in args:
        with open(file_path, encoding=encoding) as file:
            for number, line in enumerate(file, start=1):
                line = line[:-1]  # remove "\n" at the end of each line
                pos = line.find("|")
                if pos < 0:
                    logger.warning(f"{source_str(file_path, number)} Absent splitter. Discard line: {line}")
                    continue
                key, val = line[:pos], line[pos + 1:]
                if key == "":
                    logger.warning(f"{source_str(file_path, number)} Empty key. Discard line: {line}")
                    continue
                if key in language:
                    description = f"{source_str(file_path, number)} Not unique key. Discard line"
                    if key not in dup_keys:
                        prev_val = language[key]
                        logger.warning(f"{source[key]} Duplicated key".ljust(len(description)) + f": {key}|{prev_val}")
                        dup_keys.add(key)
                    logger.warning(description + f": {line}")
                    continue
                language[key] = val
                source[key] = source_str(file_path, number)
    return language


def find_files(*args: str) -> List[str]:
    """
    Find .csv files in the given directories.

    :param args: Paths to directories in which to search for .csv files.
    :return: A list of paths to the found .csv files.
    """
    file_paths = []
    for dir_path in args:
        for file_name in os.listdir(dir_path):
            if re.fullmatch(r'.*\.csv', file_name):
                file_path = os.path.join(dir_path, file_name)
                if os.path.isfile(file_path):
                    file_path = os.path.abspath(file_path)
                    file_paths.append(file_path)
    return file_paths


__all__ = ["load_files", "find_files"]


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
            lang = load_files(*find_files(dir_path))
        except Exception as e:
            print(traceback.format_exc(), flush=True)
        for key, val in lang.items():
            print(f"{key}|{val}")
        print()

    LANG_EN_PATH = "/sandbox/MountAndBladeWarband/resources/languages/en/"
    print(f"load dir {LANG_EN_PATH}")
    file_pathes = find_files(LANG_EN_PATH)
    lang = load_files(*file_pathes)
    print()

    for key, val in list(lang.items())[::500]:
        print(f"{key}|{val}")
    print()

    key = "skl_trainer_desc"
    print(key, lang[key], sep="|")

    key = "ui_chest"
    print(key, lang[key], sep="|")
