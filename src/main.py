#!/usr/bin/python3.10

import argparse
import logging
import os
from types import MappingProxyType
from typing import Mapping

from mbw_language import LangLoader
from mbw_language.LangValParser import Interpolation
import mss
import numpy as np
from typeguard import typechecked

from DialogScreenManager.DialogScreenManager import DialogScreenManager

logger = logging.getLogger(__name__)
dialog_screen_manager = None


def init(log_level, write_to_dataset):
    import config
    # config logging
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s : %(message)s")
    logging.getLogger(DialogScreenManager.__name__).setLevel(log_level)
    # load lang
    lang = load_lang(os.path.join(config.languages_dir_path, config.language),
                     playername=config.playermane)
    # create dialog screen manager
    global dialog_screen_manager
    dialog_screen_manager = DialogScreenManager(lang, write_to_dataset)


@typechecked
def load_lang(*args: str, playername: str) -> Mapping[str, Interpolation]:
    # load lang from passed dirs
    lang_file_paths = LangLoader.find_csv(*args)
    if len(lang_file_paths) == 0:
        raise ValueError(f"No csv files found at {','.join(args)}")
    lang = LangLoader.load_files(*lang_file_paths)
    if len(lang) == 0:
        raise ValueError(f"Empty lang is loaded by {','.join(args)}")
    # update lang with special keys
    lang = lang | {"wa_player": playername}
    return MappingProxyType(lang)


def main(args):
    init(log_level=logging.DEBUG if args.verbose else logging.INFO,
         write_to_dataset=args.dataset)
    with mss.mss() as sct:
        monitor = sct.monitors[args.monitor]
        print("START")
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


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose",
                    action="store_true",
                    help="Enable verbose mode to print debug-level logs.")
parser.add_argument("-ds", "--dataset",
                    action="store_true",
                    help="Enable writing data to datasets.")
parser.add_argument("-m", "--monitor",
                    action="append", type=int, default=[],
                    help="The number of the monitor to be captured (starting from 1, default is 1).",
                    metavar="2")
parser.set_defaults(func=main)


if __name__ == "__main__":
    sys_args = parser.parse_args()
    if sys_args.monitor is not None and len(sys_args.monitor) > 1:
        parser.error("argument -m/--monitor cannot be specified twice.")
    sys_args.monitor = sys_args.monitor[0] if sys_args.monitor else 1
    sys_args.func(sys_args)
