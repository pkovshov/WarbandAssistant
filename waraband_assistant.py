#!/usr/bin/python3

import argparse
import logging
import os
import sys

scrip_dir_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(scrip_dir_path)
sys.path.append(os.path.abspath(os.path.join(scrip_dir_path, 'src')))

from wa_screen_manager.GameScreenManager import GameScreenManager
import wa_screen_manager, wa_datasets, wa_language


def main(args):
    # config logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s : %(message)s")
    logging.getLogger(wa_screen_manager.__name__).setLevel(log_level)
    logging.getLogger(wa_datasets.__name__).setLevel(log_level)
    logging.getLogger(wa_language.__name__).setLevel(log_level)
    logging.getLogger(__name__).setLevel(log_level)
    # process player name
    playername = args.player
    # create GameScreenManager
    write_to_dataset = args.dataset
    game_Screen_manager = GameScreenManager(playername=playername,
                                            write_to_dataset=write_to_dataset)
    # run
    monitor = args.monitor
    print("START", "datasets", "ON" if write_to_dataset else "OFF")
    try:
        game_Screen_manager.run(monitor)
    except KeyboardInterrupt:
        print("\b\b  \b\b", end="")
        print("STOP")


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
