import re

from typeguard import typechecked


__title_checkers = []


def title(func):
    @typechecked
    def wrapper(key: str) -> bool:
        return func(key)
    __title_checkers.append(wrapper)
    return wrapper


def is_title(key):
    return any(checker(key) for checker in __title_checkers)


@title
def is_king(key):
    return re.fullmatch(r"trp_kingdom_\d_lord_pl", key) is not None


@title
def is_lord(key):
    return re.fullmatch(r"trp_knight_\d_\d+\d?_pl", key) is not None


@title
def is_lady(key):
    return (re.fullmatch(r"trp_kingdom_\d_lady_\d+\d?_pl", key) is not None or
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


@title
def is_npc(key):
    return re.fullmatch(r"trp_npc\d+\d?", key) is not None


@title
def is_guild_master(key):
    return re.fullmatch(r"trp_town_\d+\d?_mayor", key) is not None


@title
def is_tavern_keeper(key):
    return re.fullmatch(r"trp_town_\d+\d?_tavernkeeper", key) is not None


@title
def is_tournament_master(key):
    return re.fullmatch(r"trp_town_\d+\d?_arena_master", key) is not None


@title
def is_weaponsmith(key):
    return re.fullmatch(r"trp_town_\d+\d?_weaponsmith", key) is not None


@title
def is_armorer(key):
    return re.fullmatch(r"trp_town_\d+\d?_armorer", key) is not None


@title
def is_armorer(key):
    return re.fullmatch(r"trp_town_\d+\d?_armorer", key) is not None


@title
def is_horse_merchant(key):
    return re.fullmatch(r"trp_town_\d+\d?_horse_merchant", key) is not None


@title
def is_merchant(key):
    return re.fullmatch(r"trp_town_\d+\d?_merchant", key) is not None


@title
def is_town_walker(key):
    return key in ("trp_town_walker_1",
                   "trp_town_walker_2")


@title
def is_village_elder(key):
    return re.fullmatch(r"trp_village_\d{1,3}_elder", key) is not None


@title
def is_village_walker(key):
    return key in ("trp_village_walker_1",
                   "trp_village_walker_2")


if __name__ == "__main__":
    print(is_lord("b1"))
    print(is_title("b"))
