from collections import namedtuple

from wa_datasets.MapCalendarsDataset import MapCalendarsDataset

dataset = MapCalendarsDataset(lazy_load=True)

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
    if "calendar_overlapped" not in data:
        data["calendar_overlapped"] = None
    meta = MetaItem(**data)
    dataset.replace_meta(idx, meta)
