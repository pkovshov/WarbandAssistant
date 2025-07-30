import logging
from typing import NamedTuple, Optional, Tuple

import rapidfuzz as fz
from wa_typechecker import typechecked

from wa_language.Language import Language
from wa_language.LangKey import LangKey
from wa_language.LangVar import PlayerSex
from wa_model.LangModel import SexLangValueModel
from wa_model.dialog_model.LangDialogModel import LangDialogModel

from .DialogScreenEvent import DialogBodyBound


TEXT = 0
SCORE = 1
KEY = 2


class KeyAndSex(NamedTuple):
    key: LangKey
    sex: Optional[PlayerSex]


class DialogBodyFuzzyParser:
    @typechecked
    def __init__(self, lang: Language, player_sex: Optional[PlayerSex]):
        from . import dialog_screen_config
        self.__logger = logging.getLogger(__name__)
        self.__model = LangDialogModel(lang=lang,
                                       player_sex=player_sex)
        self.__sex_spread_model = SexLangValueModel()
        self.__prev_body_ocr = None
        self.__prev_title_keys = None
        self.__prev_body_bound = None


    @typechecked
    def bound(self, body_ocr: str, title_keys: Tuple[LangKey, ...]) -> Tuple[DialogBodyBound, ...]:
        if body_ocr != self.__prev_body_ocr or title_keys != self.__prev_title_keys:
            self.__prev_body_ocr = body_ocr
            self.__prev_title_keys = title_keys
            self.__prev_body_bound = self.__bound(body_ocr, title_keys)
        return self.__prev_body_bound

    def __bound(self, body_ocr: str, title_keys: Tuple[LangKey, ...]) -> Tuple[DialogBodyBound, ...]:
        body_keys = set().union(*(self.__model.get_body_keys(title_key)
                                  for title_key in title_keys))
        # build body_lang_sex_spread with dummy None sex
        body_lang_sex_spread = {KeyAndSex(sex=None, key=key): self.__model.get_value(key)
                                for key in body_keys}
        # make a real sex spreading if sex is not set in model
        if self.__model.player_sex is None:
            new_body_lang_sex_spread = {}
            for key_and_none_sex, val in body_lang_sex_spread.items():
                spread = self.__sex_spread_model.spread(val)
                if spread[PlayerSex.MALE] == spread[PlayerSex.FEMALE]:
                    new_body_lang_sex_spread[key_and_none_sex] = val
                else:
                    new_body_lang_sex_spread[KeyAndSex(key=key_and_none_sex.key,
                                                       sex=PlayerSex.MALE)] = spread[PlayerSex.MALE]
                    new_body_lang_sex_spread[KeyAndSex(key=key_and_none_sex.key,
                                                       sex=PlayerSex.FEMALE)] = spread[PlayerSex.FEMALE]
            body_lang_sex_spread = new_body_lang_sex_spread

        matches = fz.process.extract(query=body_ocr,
                                     scorer=fz.fuzz.ratio,
                                     choices=body_lang_sex_spread,
                                     score_cutoff=80,
                                     limit=len(body_lang_sex_spread))
        if len(matches) == 0:
            return tuple()
        # filter best matches
        best_score = matches[0][SCORE]
        matches = [match for match in matches if match[SCORE] == best_score]
        # check that all best matches have the same text
        best_text = matches[0][TEXT]
        for match in matches:
            if match[TEXT] != best_text:
                self.__logger.warning(f"best matches have different texts: '{best_text}' and 'match[TEXT]'")
                break
        # check that matches has no unbinded variables
        # current implementation does not work with such strings
        for match in matches:
            if len(match[TEXT].variables) > 0:
                raise NotImplemented("Do not use Interpolations with variables other then PlayerSexVar")
        # build boundaries
        boundary_keys = tuple(match[KEY].key for match in matches)
        # normally we should have only one best match
        if len(boundary_keys) > 1:
            self.__logger.warning("Got {} best matches with keys {} for dialog title keys {}"
                                  .format(len(boundary_keys),
                                          ", ".join(boundary_keys),
                                          ", ".join(title_keys)))
        boundaries = tuple(DialogBodyBound(key=key, bind={}) for key in boundary_keys)
        return boundaries
