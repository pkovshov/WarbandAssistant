import itertools
import logging

from wa_typechecker import typechecked
from wa_language.Language import Language
from wa_language.LangKey import LangKey
from wa_language.LangVar import PlayerSex
from wa_language.LangValue import LangValue
from wa_model.dialog_model.DialogBodyModel import DialogBodyModel
from ..BaseScreen.ModelFuzzyParser import ModelFuzzyParser, isclose


class DialogBodyFuzzyParser:
    @typechecked
    def __init__(self, lang: Language, player_sex: PlayerSex | None):
        self.__logger = logging.getLogger(__name__)
        self.__dialog_body_model = DialogBodyModel(language=lang,
                                                   player_name=None,
                                                   player_sex=player_sex)
        self.__model_fuzzy_parser = ModelFuzzyParser(score_cutoff=80)
        self.__prev_body_ocr = None
        self.__prev_title_keys = None
        self.__prev_body_bound = None


    @typechecked
    def bounds(self, body_ocr: str, title_keys: tuple[LangKey, ...]) -> tuple[LangValue, ...]:
        if body_ocr != self.__prev_body_ocr or title_keys != self.__prev_title_keys:
            self.__prev_body_ocr = body_ocr
            self.__prev_title_keys = title_keys
            self.__prev_body_bound = self.__bounds(body_ocr, title_keys)
        return self.__prev_body_bound

    def __bounds(self, body_ocr: str, title_keys: tuple[LangKey, ...]) -> tuple[LangValue, ...]:
        body_models = {id(model): model for model
                       in (self.__dialog_body_model.get(key) for key in title_keys)
                       if model is not None}
        if len(body_models) == 0:
            return tuple()
        body_models = list(body_models.values())
        bounds_and_scores = []
        for model in body_models:
            bounds_and_score = self.__model_fuzzy_parser.bounds(model, body_ocr)
            if bounds_and_score.bounds:
                bounds_and_scores.append(bounds_and_score)
        if len(bounds_and_scores) == 0:
            return tuple()
        best_score = max(bns.score for bns in bounds_and_scores)
        bounds = tuple(itertools.chain.from_iterable(bns.bounds for bns in bounds_and_scores
                                                     if isclose(bns.score, best_score)))
        # check that all best matches have the same text
        # TODO: remove from production, keep in dev only
        for value in bounds:
            if value != bounds[0]:
                logging.getLogger(__name__).warning(
                    f"best matches have different texts: '{bounds[0]}' and '{value}'")
                break
        return bounds
