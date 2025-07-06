"""
Look over the categories of language keys.
Focus on those that contain keys suitable for dialog titles.
"""

from os import path

from wa_language.LangLoader import *
import path_conf
from wa_language.model.troop_keys import *

lang = load_files(path.join(path_conf.language, "troops.csv"))


def print_checker_count(check, caption):
    print(str(caption) + ":",
          sum(1 for key in lang if check(key)),
          lang[next(key for key in lang if check(key))])
    print()


def print_checker_troop(check):
    val = lang[next(key for key in lang if check(key))]
    print("troop",
          val + ":",
          sum(1 for key in lang if check(key)),
          val)

def print_checker(check, caption):
    print(str(caption) + ":")
    for key, val in lang.items():
        if check(key):
            print(f"{key}|{val}")
    print(sum(1 for key in lang if check(key)))
    print()


def print_checker_and_non_pl(check, caption):
    print(str(caption) + ":")
    for key, val in lang.items():
        if check(key):
            print(f"{key}|{val}".ljust(40), "non-pl:", lang[key[:-3]])
    print(sum(1 for key in lang if check(key)))
    print()


print_checker(is_king_key, "Kings")
print_checker(is_pretender_key, "Pretenders")
print_checker_and_non_pl(is_lord_key, "Lords")
print_checker_and_non_pl(is_lady_key, "Ladies")
print_checker(is_npc_key, "NPCs")
print_checker_count(is_guild_master_key, "Guild Masters")
print_checker_count(is_tavern_keeper_key, "Tavern Keepers")
print_checker_count(is_tournament_master_key, "Tournament Masters")
print_checker_count(is_weaponsmith_key, "Weaponsmiths")
print_checker_count(is_armorer_key, "Armorers")
print_checker_count(is_horse_merchant_key, "Horse Merchants")
print_checker_count(is_goods_merchant_key, "Merchants")
print_checker_count(is_traveller_key, "Travelers")
print_checker_count(is_ransom_broker_key, "Ransom Brokers")
print_checker_count(is_minstrel_key, "Minstrels")
print_checker_count(is_book_merchant_key, "Book Merchant")
print_checker_count(is_ramun_slave_trader_key, "Ramun the slave trader")
print_checker_count(is_tavern_farmer_key, "Tavern Farmer")
print_checker_count(is_drunk_key, "Drunks")
print_checker_count(is_hired_assassin_key, "Hired Assassins")
print_checker_count(is_town_walker_key, "Townspeople")
print_checker_count(is_village_elder_key, "Village Elders")
print_checker_count(is_village_walker_key, "Villagers")
print_checker(is_quest_merchant_key, "Quest Merchants")
print_checker_count(is_quest_fugitive_key, "Fugitive")
print_checker_count(is_quest_ordinary_townsman_key, "Ordinary Townsman")
print_checker_count(is_quest_unremarkable_townsman_key, "Unremarkable Townsman")
print_checker_count(is_trainer_key, "Trainers")
print_checker_troop(is_troop_farmer_key)
print_checker_troop(is_troop_caravan_master_key)
print()
# need a config or complexity playername recognition for testing is_player check
# print_checker_count(is_player)
print_checker_count(is_troop_key, "Dialog Titles")






