from wa_language.KeyChecker import key_checker
from wa_model.types import LordPersonality
from .comment_intro_keys import *
from .private_chat_keys import *

personality_to_lord_body_checker = {
    personality: key_checker(
        key_checker(comment_intro_checker,
                    pass_filter=comment_intro_filter_by_lord_personality[personality]),
        private_chat_keys_by_lord_personality[personality])
    for personality in LordPersonality
}
