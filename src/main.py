import logging
import os

import mss
import numpy as np

from mbw_language import LangLoader

from DialogScreenManager.DialogScreenManager import DialogScreenManager
import config

logger = logging.getLogger(__name__)
dialog_screen_manager = None


def init():
    # config logging
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s : %(message)s")
    logging.getLogger(DialogScreenManager.__name__).setLevel(logging.DEBUG)
    # load lang
    lang_dir_path = os.path.join(config.languages_dir_path, config.language)
    lang_file_paths = LangLoader.find_csv(lang_dir_path)
    if len(lang_file_paths) == 0:
        raise ValueError(f"No csv files found at {lang_dir_path}")
    else:
        lang = LangLoader.load_files(*lang_file_paths)
        if len(lang) == 0:
            raise ValueError(f"Empty lang is loaded by {lang_dir_path}")
    # create dialog screen manager
    global dialog_screen_manager
    dialog_screen_manager = DialogScreenManager(lang)


def main():
    init()
    with mss.mss() as sct:
        monitor = sct.monitors[config.monitor_idx]
        try:
            run(sct, monitor)
        except KeyboardInterrupt:
            print("\b\b  \b\b", end="")
            print("STOP")



def run(sct, monitor):
    while True:
        scr = sct.grab(monitor)
        img = np.array(scr)[:, :, :3]  # BGRA -> BGR
        dialog_screen_manager.process(img)


if __name__ == "__main__":
    main()
