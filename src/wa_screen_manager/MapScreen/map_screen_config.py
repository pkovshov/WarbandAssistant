from os import path

import path_conf
from wa_types import Box

map_screen_blank_img_path = path.join(path_conf.samples,
                                      "map_screen_blank.png")

__map_menu_top = 1008
__map_menu_bottom = 1080
map_calendar_box = Box(1540, 1016, 1920, 1080)
# all three boxes need to confirm that the map calendar is not overlapped
map_calendar_sample_boxes = (
    (Box(map_calendar_box.l, map_calendar_box.t, map_calendar_box.l+6, map_calendar_box.b),
     Box(map_calendar_box.r-6, map_calendar_box.t, map_calendar_box.r, map_calendar_box.b),
     Box(map_calendar_box.l, __map_menu_top, map_calendar_box.r, __map_menu_top+6),
     ),
)
# each box could confirm that it's a map screen
map_screen_sample_boxes = (
    (Box(407, __map_menu_top, 413, __map_menu_bottom),),
    (Box(630, __map_menu_top, 636, __map_menu_bottom),),
    (Box(852, __map_menu_top, 859, __map_menu_bottom),),
    (Box(1075, __map_menu_top, 1081, __map_menu_bottom),),
    (Box(1298, __map_menu_top, 1304, __map_menu_bottom),),
    (Box(1519, __map_menu_top, 1524, __map_menu_bottom),),
    (Box(1540, __map_menu_top, 1546, __map_menu_bottom),),
    (Box(1914, __map_menu_top, 1920, __map_menu_bottom),),
)
