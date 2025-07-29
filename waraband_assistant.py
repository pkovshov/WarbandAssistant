#!/usr/bin/python3

import argparse
import logging
import os
import sys

scrip_dir_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(scrip_dir_path)
sys.path.append(os.path.abspath(os.path.join(scrip_dir_path, 'src')))

from wa_language.Binding import PlayerSex
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
    game_Screen_manager = GameScreenManager(player_name=args.playername,
                                            player_sex=args.playersex,
                                            datasets=args.datasets)
    # run
    monitor = args.monitor
    if args.datasets:
        print("START", "datasets:", ", ".join(args.datasets))
    else:
        print("START", "datasets", "OFF")
    try:
        game_Screen_manager.run(monitor)
    except KeyboardInterrupt:
        print("\b\b  \b\b", end="")
        print("STOP")


class UniqueOnceAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            parser.error(f"Option {option_string} specified more than once")
        setattr(namespace, self.dest, values)


DATASET_ALIASES = {
    "db": "dialog_bodies",
    "dr": "dialog_relations",
    "dt": "dialog_titles",
    "mc": "map_calendars",
}

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose",
                    action="store_true",
                    help="Enable verbose mode to print debug-level logs.")
parser.add_argument("-ds", "--datasets",
                    action=UniqueOnceAction, nargs="*",
                    help="Datasets to use. Available: " +
                         ", ".join(f"{val} ({key})" for key, val in DATASET_ALIASES.items()) + ". "
                         "If not specified, defaults to all the datasets.")
parser.add_argument("-m", "--monitor",
                    action="append", type=int, default=[],
                    help="The number of the monitor to be captured (starting from 1, default is 1).",
                    metavar="2")
parser.add_argument("-p", "--player",
                    dest='playername', action="append", type=str, default=[],
                    help="A player name",
                    metavar="'Sid Neil'")
parser_sex_group = parser.add_mutually_exclusive_group()
parser_sex_group.add_argument('-male', '--male',
                              dest='playersex', action='store_const', const=PlayerSex.MALE,
                              help='Male player sex')
parser_sex_group.add_argument('-female', '--female',
                              dest='playersex', action='store_const', const=PlayerSex.FEMALE,
                              help='Female player sex')
parser.set_defaults(func=main)


if __name__ == "__main__":
    sys_args = parser.parse_args()
    if sys_args.monitor is not None and len(sys_args.monitor) > 1:
        parser.error("argument -m/--monitor cannot be specified twice.")
    sys_args.monitor = sys_args.monitor[0] if sys_args.monitor else 1
    if sys_args.playername is not None and len(sys_args.playername) > 1:
        parser.error("argument -p/--player cannot be specified twice.")
    sys_args.playername = sys_args.playername[0] if sys_args.playername else None
    if sys_args.datasets is None:
        sys_args.datasets = []
    elif len(sys_args.datasets) == 0:
        sys_args.datasets = list(DATASET_ALIASES.values())
    else:
        for idx, val in enumerate(sys_args.datasets):
            if val in DATASET_ALIASES:
                sys_args.datasets[idx] = val = DATASET_ALIASES[val]
            if val not in DATASET_ALIASES.values():
                parser.error(f"Invalid dataset or alias: '{val}'")
        sys_args.datasets = list(set(sys_args.datasets))
    sys_args.func(sys_args)
