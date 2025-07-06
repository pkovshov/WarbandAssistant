import re

from typeguard import typechecked


__troop_key_checkers = []

# TODO: Add enterprise's person titles that are absent in language resources
#       (dialogs in brewery, tannery, ironworks e.t.c)


def troop_key(func):
    @typechecked
    def wrapper(key: str) -> bool:
        return func(key)
    __troop_key_checkers.append(wrapper)
    return wrapper


def is_troop_key(key):
    return any(checker(key) for checker in __troop_key_checkers)


@troop_key
def is_king_key(key):
    return re.fullmatch(r"trp_kingdom_\d_lord", key) is not None


@troop_key
def is_pretender_key(key):
    return re.fullmatch(r"trp_kingdom_\d_pretender", key) is not None


@troop_key
def is_lord_key(key):
    return re.fullmatch(r"trp_knight_\d_\d\d?_pl", key) is not None


@troop_key
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


@troop_key
def is_npc_key(key):
    return re.fullmatch(r"trp_npc\d\d?", key) is not None


@troop_key
def is_guild_master_key(key):
    return re.fullmatch(r"trp_town_\d\d?_mayor", key) is not None


@troop_key
def is_tavern_keeper_key(key):
    return re.fullmatch(r"trp_town_\d\d?_tavernkeeper", key) is not None


@troop_key
def is_tournament_master_key(key):
    return re.fullmatch(r"trp_town_\d\d?_arena_master", key) is not None


@troop_key
def is_weaponsmith_key(key):
    return re.fullmatch(r"trp_town_\d\d?_weaponsmith", key) is not None


@troop_key
def is_armorer_key(key):
    return re.fullmatch(r"trp_town_\d\d?_armorer", key) is not None


@troop_key
def is_horse_merchant_key(key):
    return re.fullmatch(r"trp_town_\d\d?_horse_merchant", key) is not None


@troop_key
def is_goods_merchant_key(key):
    return re.fullmatch(r"trp_town_\d\d?_merchant", key) is not None


@troop_key
def is_traveller_key(key):
    return re.fullmatch(r"trp_tavern_traveler_\d\d?", key) is not None


@troop_key
def is_ransom_broker_key(key):
    return re.fullmatch(r"trp_ransom_broker_\d\d?", key) is not None


@troop_key
def is_minstrel_key(key):
    return re.fullmatch(r"trp_tavern_minstrel_\d", key) is not None


@troop_key
def is_book_merchant_key(key):
    return re.fullmatch(r"trp_tavern_bookseller_\d", key) is not None


@troop_key
def is_ramun_slave_trader_key(key):
    return key == "trp_ramun_the_slave_trader"


@troop_key
def is_tavern_farmer_key(key):
    return key == "trp_farmer_from_bandit_village"


@troop_key
def is_drunk_key(key):
    return key == "trp_belligerent_drunk"


def is_hired_assassin_key(key):
    return key == "trp_hired_assassin"


@troop_key
def is_town_walker_key(key):
    return key in ("trp_town_walker_1",
                   "trp_town_walker_2")


@troop_key
def is_village_elder_key(key):
    return re.fullmatch(r"trp_village_\d{1,3}_elder", key) is not None


@troop_key
def is_village_walker_key(key):
    return key in ("trp_village_walker_1",
                   "trp_village_walker_2")


@troop_key
def is_quest_merchant_key(key):
    """Quest Merchant"""
    return key in ("trp_swadian_merchant",
                   "trp_vaegir_merchant",
                   "trp_khergit_merchant",
                   "trp_nord_merchant",
                   "trp_rhodok_merchant",
                   "trp_sarranid_merchant")


@troop_key
def is_quest_fugitive_key(key):
    """Hunt Down Fugitive"""
    return key == "trp_fugitive"


@troop_key
def is_quest_ordinary_townsman_key(key):
    """Quest Follow the spy"""
    return key == "trp_spy"


@troop_key
def is_quest_unremarkable_townsman_key(key):
    """Quest Follow the spy"""
    return key == "trp_spy_partner"


@troop_key
def is_trainer_key(key):
    """Trainers in the Training fields"""
    return re.fullmatch(r"trp_trainer_\d", key) is not None


@troop_key
def is_troop_farmer_key(key):
    return key == "trp_farmer"


@troop_key
def is_troop_caravan_master_key(key):
    return key == "trp_caravan_master"


@troop_key
def is_player_key(key):
    """Special key added by WarbandAssistant"""
    return key == "wa_player"


if __name__ == "__main__":
    print(is_lord_key("b1"))
    print(is_title("b"))
