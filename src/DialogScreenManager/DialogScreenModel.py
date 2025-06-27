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







if __name__ == "__main__":
    print(is_lord("b1"))
    print(is_title("b"))
