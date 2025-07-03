from abc import ABC, abstractmethod
from typing import Optional, Tuple

import numpy as np


class DialogScreenArtifactsProcessor(ABC):
    """Base class for artifacts processors"""
    @abstractmethod
    def process(self,
                img: np.ndarray,
                sample_matches: bool,
                title_ocr: str,
                title_fuzzy_score: Optional[float],
                title_keys: Tuple[str, ...]):
        raise NotImplemented()
