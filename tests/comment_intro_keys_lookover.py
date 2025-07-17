from wa_language.Language import load
from wa_language.model.types import *
from wa_language.model.dialog_model.comment_intro_keys import *

lang = load()


print("=" * 80)
print("=", "King")
print("=" * 80)
for player_sex in (None, PlayerSex.MALE, PlayerSex.FEMALE):
    print("player_sex:", None if player_sex is None else player_sex.name)
    checker = build_king_comment_intro_checker(player_sex)(lang)
    for key, val in checker.items():
        print(f"{key}|{val[:80]}")
    print(len(checker))
    print()

print("=" * 80)
print("=", "Lords")
print("=" * 80)
for player_sex in (None, PlayerSex.MALE, PlayerSex.FEMALE):
    print("player_sex:", None if player_sex is None else player_sex.name)
    checker = build_lord_comment_intro_checker(player_sex=player_sex)(lang)
    for key, val in checker.items():
        print(f"{key}|{val[:80]}")
    print(len(checker))
    print()

for lord_personality in LordPersonality:
    print("=" * 80)
    print("=", lord_personality.value.capitalize())
    print("=" * 80)
    for player_sex in (None, PlayerSex.MALE, PlayerSex.FEMALE):
        print("player_sex:", None if player_sex is None else player_sex.name)
        checker = build_lord_comment_intro_checker(lord_personality=lord_personality,
                                                   player_sex=player_sex)(lang)
        for key, val in checker.items():
            print(f"{key}|{val[:80]}")
        print(len(checker))
        print()
