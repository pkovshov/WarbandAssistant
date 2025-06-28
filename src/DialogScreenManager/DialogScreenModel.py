import re

from typeguard import typechecked


__title_checkers = []

# TODO: Add enterprise's person titles that are absent in language resources
#       (dialogs in brewery, tannery, ironworks e.t.c)


def dialog_title(func):
    @typechecked
    def wrapper(key: str) -> bool:
        return func(key)
    __title_checkers.append(wrapper)
    return wrapper


def is_dialog_title_key(key):
    return any(checker(key) for checker in __title_checkers)


@dialog_title
def is_king(key):
    return re.fullmatch(r"trp_kingdom_\d_lord", key) is not None


@dialog_title
def is_pretender(key):
    return re.fullmatch(r"trp_kingdom_\d_pretender", key) is not None


@dialog_title
def is_lord(key):
    return re.fullmatch(r"trp_knight_\d_\d\d?_pl", key) is not None


@dialog_title
def is_lady(key):
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


@dialog_title
def is_npc(key):
    return re.fullmatch(r"trp_npc\d\d?", key) is not None


@dialog_title
def is_guild_master(key):
    return re.fullmatch(r"trp_town_\d\d?_mayor", key) is not None


@dialog_title
def is_tavern_keeper(key):
    return re.fullmatch(r"trp_town_\d\d?_tavernkeeper", key) is not None


@dialog_title
def is_tournament_master(key):
    return re.fullmatch(r"trp_town_\d\d?_arena_master", key) is not None


@dialog_title
def is_weaponsmith(key):
    return re.fullmatch(r"trp_town_\d\d?_weaponsmith", key) is not None


@dialog_title
def is_armorer(key):
    return re.fullmatch(r"trp_town_\d\d?_armorer", key) is not None


@dialog_title
def is_horse_merchant(key):
    return re.fullmatch(r"trp_town_\d\d?_horse_merchant", key) is not None


@dialog_title
def is_goods_merchant(key):
    return re.fullmatch(r"trp_town_\d\d?_merchant", key) is not None


@dialog_title
def is_traveller(key):
    return re.fullmatch(r"trp_tavern_traveler_\d\d?", key) is not None


@dialog_title
def is_ransom_broker(key):
    return re.fullmatch(r"trp_ransom_broker_\d\d?", key) is not None


@dialog_title
def is_minstrel(key):
    return re.fullmatch(r"trp_tavern_minstrel_\d", key) is not None


@dialog_title
def is_book_merchant(key):
    return re.fullmatch(r"trp_tavern_bookseller_\d", key) is not None


@dialog_title
def is_ramun_slave_trader(key):
    return key == "trp_ramun_the_slave_trader"


@dialog_title
def is_tavern_farmer(key):
    return key == "trp_farmer_from_bandit_village"


@dialog_title
def is_drunk(key):
    return key == "trp_belligerent_drunk"


def is_hired_assassin(key):
    return key == "trp_hired_assassin"


@dialog_title
def is_town_walker(key):
    return key in ("trp_town_walker_1",
                   "trp_town_walker_2")


@dialog_title
def is_village_elder(key):
    return re.fullmatch(r"trp_village_\d{1,3}_elder", key) is not None


@dialog_title
def is_village_walker(key):
    return key in ("trp_village_walker_1",
                   "trp_village_walker_2")


@dialog_title
def is_quest_merchant(key):
    """Quest Merchant"""
    return key in ("trp_swadian_merchant",
                   "trp_vaegir_merchant",
                   "trp_khergit_merchant",
                   "trp_nord_merchant",
                   "trp_rhodok_merchant",
                   "trp_sarranid_merchant")


@dialog_title
def is_quest_ordinary_townsman(key):
    """Quest Follow the spy"""
    return key == "trp_spy"


@dialog_title
def is_quest_unremarkable_townsman(key):
    """Quest Follow the spy"""
    return key == "trp_spy_partner"


@dialog_title
def is_troop_farmer(key):
    return key == "trp_farmer"


@dialog_title
def is_troop_caravan_master(key):
    return key == "trp_caravan_master"


@dialog_title
def is_player(key):
    """Special key added by WarbandAssistant"""
    return key == "wa_player"


if __name__ == "__main__":
    print(is_lord("b1"))
    print(is_title("b"))
