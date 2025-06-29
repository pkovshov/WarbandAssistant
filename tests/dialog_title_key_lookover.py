from os import path

from mbw_language.LangLoader import *

import config
from DialogScreenManager.DialogScreenModel import *

lang = load_files(path.join(config.languages_dir_path, config.language, "troops.csv"))


def test_checker_count(check, caption):
    print(str(caption) + ":",
          sum(1 for key in lang if check(key)),
          lang[next(key for key in lang if check(key))])
    print()


def test_checker_troop(check):
    val = lang[next(key for key in lang if check(key))]
    print("troop",
          val + ":",
          sum(1 for key in lang if check(key)),
          val)

def test_checker(check, caption):
    print(str(caption) + ":")
    for key, val in lang.items():
        if check(key):
            print(f"{key}|{val}")
    print(sum(1 for key in lang if check(key)))
    print()


def test_checker_and_non_pl(check, caption):
    print(str(caption) + ":")
    for key, val in lang.items():
        if check(key):
            print(f"{key}|{val}".ljust(40), "non-pl:", lang[key[:-3]])
    print(sum(1 for key in lang if check(key)))
    print()


test_checker(is_king, "Kings")
test_checker(is_pretender, "Pretenders")
test_checker_and_non_pl(is_lord, "Lords")
test_checker_and_non_pl(is_lady, "Ladies")
test_checker(is_npc, "NPCs")
test_checker_count(is_guild_master, "Guild Masters")
test_checker_count(is_tavern_keeper, "Tavern Keepers")
test_checker_count(is_tournament_master, "Tournament Masters")
test_checker_count(is_weaponsmith, "Weaponsmiths")
test_checker_count(is_armorer, "Armorers")
test_checker_count(is_horse_merchant, "Horse Merchants")
test_checker_count(is_goods_merchant, "Merchants")
test_checker_count(is_traveller, "Travelers")
test_checker_count(is_ransom_broker, "Ransom Brokers")
test_checker_count(is_minstrel, "Minstrels")
test_checker_count(is_book_merchant, "Book Merchant")
test_checker_count(is_ramun_slave_trader, "Ramun the slave trader")
test_checker_count(is_tavern_farmer, "Tavern Farmer")
test_checker_count(is_drunk, "Drunks")
test_checker_count(is_hired_assassin, "Hired Assassins")
test_checker_count(is_town_walker, "Townspeople")
test_checker_count(is_village_elder, "Village Elders")
test_checker_count(is_village_walker, "Villagers")
test_checker(is_quest_merchant, "Quest Merchants")
test_checker_count(is_quest_fugitive, "Fugitive")
test_checker_count(is_quest_ordinary_townsman, "Ordinary Townsman")
test_checker_count(is_quest_unremarkable_townsman, "Unremarkable Townsman")
test_checker_count(is_trainer, "Trainers")
test_checker_troop(is_troop_farmer)
test_checker_troop(is_troop_caravan_master)
print()
# need a config or complexity playername recognition for testing is_player check
# test_checker_count(is_player)
test_checker_count(is_dialog_title_key, "Dialog Titles")






