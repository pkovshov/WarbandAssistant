from typing import Optional, Tuple

import numpy as np
from wa_typechecker import typechecked

from wa_language.LangKey import LangKey
from wa_language.LangValue import LangValue
from wa_screen_manager.GameScreenEvent import GameScreenEvent


class DialogScreenEvent(GameScreenEvent):
    @typechecked
    def __init__(self,
                 image: np.ndarray,
                 title_ocr: str,
                 title_ocr_prep: str,
                 title_keys: Tuple[LangKey, ...],
                 body_ocr: Optional[str],
                 body_bounds: tuple[LangValue, ...],
                 relation_ocr: Optional[str],
                 relation: Optional[int],
                 ):
        if relation_ocr is None:
            assert relation is None
        self.__image = image
        self.__title_ocr = title_ocr
        self.__title_ocr_prep = title_ocr_prep
        self.__title_keys = title_keys
        self.__body_ocr = body_ocr
        self.__body_bounds = body_bounds
        self.__relation_ocr = relation_ocr
        self.__relation = relation

    def __eq__(self, other):
        if not isinstance(other, DialogScreenEvent):
            return NotImplemented
        # suppose that ocr provides same result for the same image
        # suppose that fuzzy provides same result for the same input
        return (self.__title_ocr == other.__title_ocr and
                self.__body_ocr == other.__body_ocr and
                self.__relation_ocr == other.__relation_ocr)

    @property
    @typechecked
    def image(self) -> np.ndarray: return self.__image

    @property
    @typechecked
    def title_ocr(self) -> str: return self.__title_ocr

    @property
    @typechecked
    def title_ocr_prep(self) -> str: return self.__title_ocr_prep

    @property
    @typechecked
    def title_keys(self) -> Tuple[LangKey, ...]: return self.__title_keys

    @property
    @typechecked
    def body_ocr(self) -> Optional[str]: return self.__body_ocr

    @property
    @typechecked
    def body_bounds(self) -> tuple[LangValue, ...]: return self.__body_bounds

    @property
    @typechecked
    def relation_ocr(self) -> Optional[str]: return self.__relation_ocr

    @property
    @typechecked
    def relation(self) -> Optional[int]: return self.__relation
