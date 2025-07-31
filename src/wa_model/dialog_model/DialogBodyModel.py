from collections.abc import Mapping
from typing import Iterator

from wa_typechecker import typechecked
from wa_language.Language import Language
from wa_language.LangKey import LangKey
from wa_language.LangVar import PlayerSex
from wa_language.KeyChecker import KeyChecker
from wa_language.Spreading import LanguageSpread, Spreading, EMPTY_SPREADING
from wa_language.LanguageModel import LanguageModel
from wa_model.types import LangModelError
from wa_model import troop_keys
from wa_screen_manager.config import whitelist_characters
from .comment_intro_keys import *
from .private_chat_keys import *
from .gossip_about_character_model import *


class DialogBodyModel(Mapping[LangKey, LanguageModel]):
    """
    Mapping from the dialog title LangKey to the corresponding dialog body LanguageModel
    """
    @typechecked
    def __init__(self,
                 language: Language,
                 player_name: Optional[str],
                 player_sex: Optional[PlayerSex]):
        self.__language = language
        self.__player_name = player_name
        self.__player_sex = player_sex
        self.__data = {}
        self.__build()

    def __getitem__(self, lang_key) -> LanguageModel:
        return self.__data[lang_key]

    def __iter__(self) -> Iterator[LangKey]:
        return iter(self.__data)

    def __contains__(self, lang_key) -> bool:
        return lang_key in self.__data

    def __len__(self) -> int:
        return len(self.__data)

    def __add_body_model(self, title_key_checker: KeyChecker, body_model: LanguageModel):
        title_lang = title_key_checker.lang(self.__language)
        if intersect := set(self.__data) & set(title_lang):
            raise LangModelError(f"title_key_checker {title_key_checker} intersects "
                                 f"with already added body models, non-uniq keys: {intersect}")
        for key in title_lang:
            self.__data[key] = body_model

    def __add_kings_bodies(self):
        king_title_checker = troop_keys.is_king_key
        king_body_model = LanguageModel(
            model={build_king_comment_intro_key_checker(player_sex=self.__player_sex):
                   EMPTY_SPREADING},
            language=self.__language,
            symbols=whitelist_characters,
            player_name=self.__player_name,
            player_sex=self.__player_sex
        )
        self.__add_body_model(king_title_checker, king_body_model)

    def __add_lords_bodies(self):
        lord_title_checker = troop_keys.is_lord_key
        lord_body_model = LanguageModel(
            model={build_lord_comment_intro_key_checker(player_sex=self.__player_sex): EMPTY_SPREADING,
                   is_private_chat_key: EMPTY_SPREADING},
            language=self.__language,
            symbols=whitelist_characters,
            player_name=self.__player_name,
            player_sex=self.__player_sex
        )
        self.__add_body_model(lord_title_checker, lord_body_model)

    def __add_citizens_and_villagers_bodies(self):
        citizens_and_villagers_keys = key_checker(troop_keys.is_town_walker_key,
                                                  troop_keys.is_village_walker_key)
        citizens_and_villagers_body_model = LanguageModel(
            model={
                gossip_about_character_keys:
                    Spreading({
                        GOSSIP_ABOUT_CHARACTER_LORD_VAR:
                            LanguageSpread(troop_keys.is_lord_key.lang(self.__language))
                    })
            },
            language = self.__language,
            symbols = whitelist_characters,
            player_name = self.__player_name,
            player_sex = self.__player_sex
        )
        self.__add_body_model(citizens_and_villagers_keys, citizens_and_villagers_body_model)

    def __build(self):
        self.__add_kings_bodies()
        self.__add_lords_bodies()
        self.__add_citizens_and_villagers_bodies()
