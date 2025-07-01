from Box import Box

blank_img_path = "/sandbox/MountAndBladeWarband/resources/blanks/dialog_screen.png"

# Right top and right bottom corners.
# Requires two samples for reliable matching in case of screen tearing.
sample_boxes = (Box(1890, 0, 1920, 20),
                Box(1890, 1060, 1920, 1080))
