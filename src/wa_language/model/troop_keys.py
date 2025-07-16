import re

from .LangKeyChecker import key_checker

# TODO: Add enterprise's person titles that are absent in language resources
#       (dialogs in brewery, tannery, ironworks e.t.c)


__troop_key_checkers = []


def troop_key_checker(*arg):
    wrapper = key_checker(*arg)
    __troop_key_checkers.append(wrapper)
    return wrapper


########################################################################################################################
# Characters
########################################################################################################################
@troop_key_checker
def is_king_key(key):
    return re.fullmatch(r"trp_kingdom_\d_lord", key) is not None


@troop_key_checker
def is_pretender_key(key):
    return re.fullmatch(r"trp_kingdom_\d_pretender", key) is not None


@troop_key_checker
def is_lord_key(key):
    return re.fullmatch(r"trp_knight_\d_\d\d?_pl", key) is not None


@troop_key_checker
def is_lady_key(key):
    return (re.fullmatch(r"trp_kingdom_\d_lady_\d\d?_pl", key) is not None or
            key in ("trp_knight_1_lady_3_pl",
                    "trp_knight_1_lady_4_pl",
                    "trp_kingdom_l_lady_5_pl",
                    "trp_kingdom_l_lady_13_pl",
                    "trp_knight_4_2b_daughter_1_pl",
                    "trp_knight_4_2c_wife_1_pl",
                    "trp_knight_4_2c_daughter_pl",
                    "trp_knight_4_1b_wife_pl",
                    "trp_knight_4_1b_daughter_pl",
                    "trp_knight_4_2b_daughter_2_pl",
                    "trp_knight_4_2c_wife_2_pl",
                    "trp_knight_4_1c_daughter_pl",
                    "trp_kingdom_5_5_wife_pl",
                    "trp_kingdom_5_2b_wife_1_pl",
                    "trp_kingdom_5_1c_daughter_1_pl",
                    "trp_kingdom_5_2c_daughter_1_pl",
                    "trp_kingdom_5_1c_wife_1_pl",
                    "trp_kingdom_5_2c_wife_1_pl",
                    "trp_kingdom_5_1c_daughter_2_pl",
                    "trp_kingdom_5_2c_daughter_2_pl",
                    "trp_kingdom_5_1b_wife_pl",
                    "trp_kingdom_5_2b_wife_2_pl",
                    "trp_kingdom_5_1c_daughter_3_pl",
                    "trp_kingdom_5_1c_wife_2_pl",
                    "trp_kingdom_5_2c_wife_2_pl",
                    "trp_kingdom_5_1c_daughter_4_pl"))


@troop_key_checker
def is_npc_key(key):
    return re.fullmatch(r"trp_npc\d\d?", key) is not None


########################################################################################################################
# Towns people
########################################################################################################################
@troop_key_checker
def is_guild_master_key(key):
    return re.fullmatch(r"trp_town_\d\d?_mayor", key) is not None


@troop_key_checker
def is_tavern_keeper_key(key):
    return re.fullmatch(r"trp_town_\d\d?_tavernkeeper", key) is not None


@troop_key_checker
def is_tournament_master_key(key):
    return re.fullmatch(r"trp_town_\d\d?_arena_master", key) is not None


@troop_key_checker
def is_weaponsmith_key(key):
    return re.fullmatch(r"trp_town_\d\d?_weaponsmith", key) is not None


@troop_key_checker
def is_armorer_key(key):
    return re.fullmatch(r"trp_town_\d\d?_armorer", key) is not None


@troop_key_checker
def is_horse_merchant_key(key):
    return re.fullmatch(r"trp_town_\d\d?_horse_merchant", key) is not None


@troop_key_checker
def is_goods_merchant_key(key):
    return re.fullmatch(r"trp_town_\d\d?_merchant", key) is not None


@troop_key_checker
def is_traveller_key(key):
    return re.fullmatch(r"trp_tavern_traveler_\d\d?", key) is not None


@troop_key_checker
def is_ransom_broker_key(key):
    return re.fullmatch(r"trp_ransom_broker_\d\d?", key) is not None


@troop_key_checker
def is_minstrel_key(key):
    return re.fullmatch(r"trp_tavern_minstrel_\d", key) is not None


@troop_key_checker
def is_book_merchant_key(key):
    return re.fullmatch(r"trp_tavern_bookseller_\d", key) is not None


is_ramun_slave_trader_key = troop_key_checker("trp_ramun_the_slave_trader")

is_drunk_key = troop_key_checker("trp_belligerent_drunk")

is_hired_assassin_key = troop_key_checker("trp_hired_assassin")

is_town_walker_key = troop_key_checker("trp_town_walker_1",
                                       "trp_town_walker_2")


########################################################################################################################
# Villages people
########################################################################################################################
@troop_key_checker
def is_village_elder_key(key):
    return re.fullmatch(r"trp_village_\d{1,3}_elder", key) is not None


is_village_walker_key = troop_key_checker("trp_village_walker_1",
                                          "trp_village_walker_2")


########################################################################################################################
# Training Fields people
########################################################################################################################
@troop_key_checker
def is_trainer_key(key):
    """Trainers in the Training fields"""
    return re.fullmatch(r"trp_trainer_\d", key) is not None


########################################################################################################################
# Quest characters
########################################################################################################################
# Quest Save the Village
is_quest_farmer_key = troop_key_checker("trp_farmer_from_bandit_village")

# Quest Merchant
is_quest_merchant_key = troop_key_checker("trp_swadian_merchant",
                                          "trp_vaegir_merchant",
                                          "trp_khergit_merchant",
                                          "trp_nord_merchant",
                                          "trp_rhodok_merchant",
                                          "trp_sarranid_merchant")

# Hunt Down Fugitive
is_quest_fugitive_key = troop_key_checker("trp_fugitive")

# Quest Follow the spy
is_quest_ordinary_townsman_key = troop_key_checker("trp_spy")
is_quest_unremarkable_townsman_key = troop_key_checker("trp_spy_partner")


########################################################################################################################
# Troops
########################################################################################################################
# Sellswords
is_troop_farmer_key = troop_key_checker("trp_farmer")
is_troop_caravan_master_key = troop_key_checker("trp_caravan_master")

########################################################################################################################
# Special keys added by WarbandAssistant
########################################################################################################################
# Player
is_player_key = troop_key_checker("wa_player")


########################################################################################################################
# Check for any troop keys registered above in current module
########################################################################################################################
is_troop_key = key_checker(__troop_key_checkers)


if __name__ == "__main__":
    print(is_lord_key("b1"))
    print(is_troop_key("b"))
