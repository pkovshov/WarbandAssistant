#!/usr/bin/python3

import argparse
import logging
import os
import sys
from types import MappingProxyType
from typing import Mapping, Optional

import mss
import numpy as np
from typeguard import typechecked

scrip_dir_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(scrip_dir_path)
sys.path.append(os.path.abspath(os.path.join(scrip_dir_path, 'src')))

from wa_language import LangLoader
from wa_language.LangValParser import Interpolation
from wa_screen_manager.DialogScreen.DialogScreenManager import DialogScreenManager
from wa_screen_manager import DialogScreen

logger = logging.getLogger(__name__)
dialog_screen_manager = None


def init(log_level, write_to_dataset, playername, force_parsing):
    from wa_screen_manager import config
    # config logging
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s : %(message)s")
    logging.getLogger(DialogScreen.__name__).setLevel(log_level)
    logging.getLogger(__name__).setLevel(log_level)
    # process player name
    if playername is None:
        playername = config.playername
    if playername is None:
        logger.info(f"playername NOT defined")
    else:
        logger.info(f"playername = {repr(playername)}")
    # TODO: someone need to warn if playername is blank string like '  '
    #       such name could broke fuzzy
    # TODO: warn if playername equal with other dialog titles (lorn names for example)
    #       or maybe is part of other dialog titles (Merchant for example)
    #       Also it needs to process such cases in DialogScreen
    # load lang
    lang = load_lang(playername=playername)
    # create dialog screen manager
    global dialog_screen_manager
    dialog_screen_manager = DialogScreenManager(lang, write_to_dataset, playername, force_parsing)


@typechecked
def load_lang(playername: Optional[str]) -> Mapping[str, Interpolation]:
    lang = LangLoader.load_lang()
    # TODO: extend load_files with a param accepting a dict with special keys
    # update lang with special keys
    if playername is not None:
        lang = lang | {"wa_player": Interpolation(playername, raw=True)}
    return MappingProxyType(lang)


def main(args):
    init(log_level=logging.DEBUG if args.verbose else logging.INFO,
         write_to_dataset=args.dataset,
         playername=args.player,
         force_parsing=args.force_parsing)
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
parser.add_argument("-fp", "--force-parsing",
                    action="store_true",
                    help="Make OCR and fuzzy even is sample does not match.")
parser.add_argument("-m", "--monitor",
                    action="append", type=int, default=[],
                    help="The number of the monitor to be captured (starting from 1, default is 1).",
                    metavar="2")
parser.add_argument("-p", "--player",
                    action="append", type=str, default=[],
                    help="A player name",
                    metavar="'Sid Neil'")
parser.set_defaults(func=main)


if __name__ == "__main__":
    sys_args = parser.parse_args()
    if sys_args.monitor is not None and len(sys_args.monitor) > 1:
        parser.error("argument -m/--monitor cannot be specified twice.")
    sys_args.monitor = sys_args.monitor[0] if sys_args.monitor else 1
    if sys_args.player is not None and len(sys_args.player) > 1:
        parser.error("argument -m/--monitor cannot be specified twice.")
    sys_args.player = sys_args.player[0] if sys_args.player else None
    sys_args.func(sys_args)
