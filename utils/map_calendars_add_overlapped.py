from collections import namedtuple

from wa_datasets.MapScreen.MapCalendarDataset import MapCalendarDataset

dataset = MapCalendarDataset(lazy_load=True)

MetaItem = namedtuple("MetaItem",
                      "verification, "
                      "resolution, "
                      "language, "                      
                      "crop, "                      
                      "calendar_ocr, "
                      "calendar_overlapped, "
                      "date_key, "
                      "year, "
                      "day, "
                      "timeofday_key, "
                      "git_branch, "
                      "git_commit, "
                      "git_has_modified")

for idx, (meta, _) in dataset.meta_and_image_path().items():
    data = dataset._meta_to_data(meta)
    data["calendar_overlapped"] = None
    meta = MetaItem(**data)
    dataset.replace_meta(idx, meta)
