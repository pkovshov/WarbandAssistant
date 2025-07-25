"""Categories of intro comment keys

Lord or Liege talks intro comment at first meet with player.
Intro comment depends on player sec, renown and noble status.
Also, intro comment depends on Lord personality.
"""

from typing import Optional

from wa_typechecker import typechecked

from wa_language.model.types import PlayerSex, LordPersonality
from wa_language.Language import LangKey
from wa_language.model.LangKeyChecker import key_checker

comment_intro_player_famous_checker = key_checker(lambda key: (key.startswith("str_comment_intro_famous_")))
comment_intro_player_noble_checker = key_checker(lambda key: (key.startswith("str_comment_intro_noble_")))
comment_intro_player_common_checker = key_checker(lambda key: (key.startswith("str_comment_intro_common_")))

comment_intro_all_sex_checker = key_checker(comment_intro_player_famous_checker,
                                             comment_intro_player_noble_checker,
                                             comment_intro_player_common_checker)

comment_intro_player_female_only_checker = key_checker(lambda key: key.startswith("str_comment_intro_female_"))

comment_intro_checker = key_checker(comment_intro_all_sex_checker, comment_intro_player_female_only_checker)

comment_intro_filter_by_lord_personality = {
    LordPersonality.MARTIAL: key_checker(lambda key: "martial" in key),
    LordPersonality.BADTEMPERED: key_checker(lambda key: "badtempered" in key),
    LordPersonality.PITILESS: key_checker(lambda key: "pitiless" in key),
    LordPersonality.CUNNING: key_checker(lambda key: "cunning" in key),
    LordPersonality.SADISTIC: key_checker(lambda key: "sadistic" in key),
    LordPersonality.GOODNATURED: key_checker(lambda key: "goodnatured" in key),
    LordPersonality.UPSTANDING: key_checker(lambda key: "upstanding" in key),
}

comment_intro_filter_king = key_checker(lambda key: "liege" in key)


@typechecked
def build_lord_comment_intro_key_checker(lord_personality: Optional[LordPersonality] = None,
                                         player_sex: Optional[PlayerSex] = None):
    checker = (comment_intro_all_sex_checker
               if player_sex is PlayerSex.MALE
               else key_checker(comment_intro_all_sex_checker, comment_intro_player_female_only_checker))
    if lord_personality is not None:
        checker = key_checker(checker, filter=comment_intro_filter_by_lord_personality[lord_personality])
    else:
        checker = key_checker(checker, exclude=comment_intro_filter_king)
    return checker


@typechecked
def build_king_comment_intro_key_checker(player_sex: Optional[PlayerSex] = None):
    checker = (comment_intro_all_sex_checker
               if player_sex is PlayerSex.MALE
               else key_checker(comment_intro_all_sex_checker, comment_intro_player_female_only_checker))
    return key_checker(checker, filter=comment_intro_filter_king)




