from os import path

import path_conf
from wa_types import Box

dialog_screen_blank_img_path = path.join(path_conf.samples,
                                         "dialog_screen_blank.png")
# Right top and right bottom corners.
# Requires two samples for reliable matching in case of screen tearing.
dialog_screen_sample_boxes = (
    (Box(1890, 0, 1920, 20), Box(1890, 1060, 1920, 1080)),
)

title_box = Box(668, 72, 1819, 118)
title_threshold = 98
fuzzy_title_score_cutoff = 75

relation_box = Box(98, 420, 312, 450)
relation_sample_boxes = (
    (Box(58, 346, 120, 365), Box(481, 639, 537, 647)),
)
