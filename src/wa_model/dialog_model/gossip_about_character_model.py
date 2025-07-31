from wa_language.KeyChecker import key_checker
from wa_language.LangVar import LangVar
from wa_model.types import LordPersonality


GOSSIP_ABOUT_CHARACTER_LORD_VAR = LangVar("s6")

gossip_about_character_keys_by_lord_personality = {
    LordPersonality.MARTIAL: key_checker("str_gossip_about_character_martial"),
    LordPersonality.BADTEMPERED: key_checker("str_gossip_about_character_quarrelsome"),
    LordPersonality.PITILESS: key_checker("str_gossip_about_character_selfrighteous"),
    LordPersonality.CUNNING: key_checker("str_gossip_about_character_cunning"),
    LordPersonality.SADISTIC: key_checker("str_gossip_about_character_sadistic"),
    LordPersonality.GOODNATURED: key_checker("str_gossip_about_character_goodnatured"),
    LordPersonality.UPSTANDING: key_checker("str_gossip_about_character_upstanding")
}

gossip_about_character_default_personality_keys = key_checker("str_gossip_about_character_default")

gossip_about_character_keys = key_checker(list(gossip_about_character_keys_by_lord_personality.values()) +
                                          [gossip_about_character_default_personality_keys])