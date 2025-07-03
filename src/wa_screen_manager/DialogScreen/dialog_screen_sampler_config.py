from os import path

from wa_screen_manager.Box import Box
import path_conf

blank_img_path = path.join(path_conf.samples,
                           "dialog_screen_blank.png")

# Right top and right bottom corners.
# Requires two samples for reliable matching in case of screen tearing.
sample_boxes = (Box(1890, 0, 1920, 20),
                Box(1890, 1060, 1920, 1080))
