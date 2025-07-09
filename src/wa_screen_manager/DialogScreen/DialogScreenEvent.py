from typing import Optional, Tuple

import numpy as np
from typeguard import typechecked


class DialogScreenEvent:
    @typechecked
    def __init__(self,
                 image: np.ndarray,
                 title_ocr: str,
                 title: str,
                 title_keys: Tuple[str, ...],
                 relation_ocr: Optional[str],
                 relation: Optional[int]):
        if relation_ocr is None:
            assert relation is None
        self.__image = image
        self.__title_ocr = title_ocr
        self.__title = title
        self.__title_keys = title_keys
        self.__relation_ocr = relation_ocr
        self.__relation = relation

    def __eq__(self, other):
        if not isinstance(other, DialogScreenEvent):
            return NotImplemented
        # suppose that ocr provides same result for the same image
        # suppose that fuzzy provides same result for the same input
        return (self.__title_ocr == other.__title_ocr and
                self.__relation_ocr == other.__relation_ocr)

    @property
    @typechecked
    def image(self) -> np.ndarray: return self.__image

    @property
    @typechecked
    def title_ocr(self) -> str: return self.__title_ocr

    @property
    @typechecked
    def title(self) -> str: return self.__title

    @property
    @typechecked
    def title_keys(self) -> Tuple[str, ...]: return self.__title_keys

    @property
    @typechecked
    def relation_ocr(self) -> Optional[str]: return self.__relation_ocr

    @property
    @typechecked
    def relation(self) -> Optional[int]: return self.__relation
