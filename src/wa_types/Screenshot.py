import numpy as np
from wa_typechecker import typechecked

from .Resolution import Resolution


@typechecked
def is_screenshot(image: np.ndarray, resolution: Resolution) -> bool:
    return (image.dtype == np.uint8 and
            image.ndim == 3 and
            image.shape[0] == resolution.height and
            image.shape[1] == resolution.width and
            image.shape[2] == 3)
