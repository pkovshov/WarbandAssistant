from typing import Dict, Set, Tuple

from typeguard import typechecked

from wa_language.Language import Language, LangKey
from wa_language.model.types import PlayerSex, LangModelError
from wa_language.model.LangKeyChecker import KeyChecker, LangKeyChecker
from wa_language.syntax.Binary import (BINARY_CONDITION_VARIABLE,
                                       BINARY_CONDITION_VARIABLE_FIRST_VALUE,
                                       BINARY_CONDITION_VARIABLE_SECOND_VALUE)
from wa_language.syntax.Interpolation import Interpolation
from .comment_intro_keys import *
from wa_language.model import troop_keys

class LangDialogModel:
    def __init__(self, lang: Language, player_sex: Optional[PlayerSex]):
        self.__lang = lang
        self.__player_sex = player_sex

        self.__title_checker_to_body_keys: Dict[KeyChecker, Tuple[LangKey, ...]] = {}
        self.__body_lang: Dict[LangKey, Interpolation] = {}

        self.__add_kings_bodies()
        self.__add_lords_bodies()

        self.__body_lang = self.substitute_sex_to_lang(self.__body_lang)

    @property
    def lang(self): return self.__lang

    @property
    def player_sex(self): return self.__player_sex

    @typechecked
    def get_body_keys(self, title_key: LangKey) -> Tuple[LangKey, ...]:
        for title_checker, body_keys in self.__title_checker_to_body_keys.items():
            if title_key in title_checker:
                return body_keys
        return tuple()

    @typechecked
    def get_value(self, key: LangKey) -> Optional[Interpolation]:
        return self.__body_lang.get(key, None)

    def __add_kings_bodies(self):
        king_title_checker = troop_keys.is_king_key
        self.assert_title_keys_uniq(king_title_checker)
        # body keys that correspond title keys from king_title_checker
        body_keys: Set[LangKey] = set()
        # process comment_intro body keys
        king_comment_intro_lang = build_king_comment_intro_key_checker(player_sex=self.__player_sex).lang(self.__lang)
        for key, val in king_comment_intro_lang.items():
            self.__body_lang[key] = val
            body_keys.add(key)
        # add king_title_checker
        body_keys = tuple(body_keys)
        self.__title_checker_to_body_keys[king_title_checker] = body_keys

    def __add_lords_bodies(self):
        lord_title_checker = troop_keys.is_lord_key
        self.assert_title_keys_uniq(lord_title_checker)
        # body keys that correspond title keys from lord_title_checker
        body_keys: Set[LangKey] = set()
        # process comment_intro body keys
        lord_comment_intro_lang = build_lord_comment_intro_key_checker(player_sex=self.__player_sex).lang(self.__lang)
        for key, val in lord_comment_intro_lang.items():
            self.__body_lang[key] = val
            body_keys.add(key)
        # add lord_title_checker
        body_keys = tuple(body_keys)
        self.__title_checker_to_body_keys[lord_title_checker] = body_keys

    @typechecked
    def assert_title_keys_uniq(self, title_checker: KeyChecker) -> None:
        title_checker_lang = title_checker.lang(self.__lang)
        match_key = self.find_match_title_key(title_checker_lang)
        if match_key is not None:
            raise LangModelError(f"Key {match_key} matches a checker from __title_key_checker_to_body_keys")

    @typechecked
    def find_match_title_key(self, title_checker_lang: LangKeyChecker) -> Optional[LangKey]:
        """
        :param self:
        :param exam_checker: A checker which keys are exams
        :return: Key is it match checkes from __title_key_checker_to_body_keys
                 None if all the examined keys are uniq
        """
        for key in title_checker_lang:
            for checker in self.__title_checker_to_body_keys:
                if key in checker:
                    return key
        return None

    @typechecked
    def substitute_sex(self, lang_val: Interpolation) -> Interpolation:
        if self.__player_sex is None:
            return lang_val
        else:
            return lang_val.substitute(BINARY_CONDITION_VARIABLE,
                                       BINARY_CONDITION_VARIABLE_FIRST_VALUE
                                       if self.__player_sex is PlayerSex.MALE
                                       else BINARY_CONDITION_VARIABLE_SECOND_VALUE)

    @typechecked
    def substitute_sex_to_lang(self, lang: Dict[LangKey, Interpolation]) -> Dict[LangKey, Interpolation]:
        return {key: self.substitute_sex(val) for key, val in lang.items()}
