import itertools
import logging
import math
from typing import NamedTuple

import rapidfuzz as fz

from wa_language.LangVar import PlayerSexVar
from wa_typechecker import typechecked
from wa_language.LangValue import LangValue
from wa_language.LanguageModel import LanguageModel


class BoundsAndScore(NamedTuple):
    bounds: tuple[LangValue, ...]
    score: float | None


EMPTY_BOUND_AND_SCORE = BoundsAndScore(bounds=tuple(), score=None)

VALUE = 0
SCORE = 1
KEY = 2

TOLERANCE = 1e-5


def isclose(score_1, score_2):
    return math.isclose(score_1, score_2, abs_tol=TOLERANCE)


class ModelFuzzyParser:
    @typechecked
    def __init__(self, score_cutoff):
        self.__score_cutoff = score_cutoff

    @typechecked
    def bounds(self, model: LanguageModel, ocr: str) -> BoundsAndScore:
        choices = model.purge_spread
        if len(choices) == 0:
            return EMPTY_BOUND_AND_SCORE
        matches = fz.process.extract(query=ocr,
                                     scorer=fz.fuzz.ratio,
                                     choices=choices,
                                     limit=len(choices))
        purge_best_score = matches[0][SCORE]
        purge_values = (match[VALUE] for match in matches
                        if isclose(match[SCORE], purge_best_score))
        result_matches = []
        for purge_value in purge_values:
            best_score = purge_best_score
            spreading = model[purge_value.key]
            value = model.language[purge_value.key]
            if PlayerSexVar in purge_value.binding and PlayerSexVar not in value.binding:
                value.bind(PlayerSexVar, purge_value.binding[PlayerSexVar])
            values = value,
            for var, spread in spreading.items():
                choices = list(itertools.chain.from_iterable(value.spread(var, spread)
                                                             for value in values))
                matches = fz.process.extract(query=ocr,
                                             scorer=fz.fuzz.ratio,
                                             choices=choices,
                                             limit=len(choices))
                best_score = matches[0][SCORE]
                values = (match[VALUE] for match in matches
                          if isclose(match[SCORE], best_score))
            if best_score >= self.__score_cutoff:
                result_matches.extend((value, best_score) for value in values)
        if result_matches:
            best_score = max(result[SCORE] for result in result_matches)
            bounds = tuple(result[VALUE] for result in result_matches
                           if isclose(result[SCORE], best_score))
            # check that all best matches have the same text
            # TODO: remove from production, keep in dev only
            for value in bounds:
                if value != bounds[0]:
                    logging.getLogger(__name__).warning(f"best matches have different texts: '{bounds[0]}' and '{value}'")
                    break
            return BoundsAndScore(bounds=bounds, score=best_score)
        else:
            return EMPTY_BOUND_AND_SCORE
