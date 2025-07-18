import logging
from typing import Optional, List

from typeguard import typechecked

from wa_datasets.DialogRelationsDataset import DialogRelationsDataset
from wa_datasets.DialogTitlesDataset import DialogTitlesDataset
from wa_datasets.MapCalendarsDataset import MapCalendarsDataset

from .DialogScreen.DialogScreenEvent import DialogScreenEvent
from .MapScreen.MapScreenEvent import MapScreenEvent


class DialogRelationDatasetProcessor:
    NAME = DialogRelationsDataset.NAME
    @typechecked
    def __init__(self):
        from .DialogScreen import dialog_screen_config
        from wa_screen_manager import config
        self.__dialog_relations_dataset = DialogRelationsDataset(resolution=config.resolution,
                                                                 crop=dialog_screen_config.relation_box,
                                                                 language=config.language)

    @typechecked
    def process(self, event: DialogScreenEvent):
        if event.relation_ocr is not None:
            self.__dialog_relations_dataset.add(screenshot=event.image,
                                                screen_sample_matches=True,
                                                relation_ocr=event.relation_ocr,
                                                relation=event.relation)


class DialogTitleDatasetProcessor:
    NAME = DialogTitlesDataset.NAME
    @typechecked
    def __init__(self, player_name: Optional[str]):
        from .DialogScreen import dialog_screen_config
        from wa_screen_manager import config
        self.__dialog_titles_dataset = DialogTitlesDataset(resolution=config.resolution,
                                                           crop=dialog_screen_config.title_box,
                                                           language=config.language,
                                                           player_name=player_name)

    @typechecked
    def process(self, event: DialogScreenEvent):
        self.__dialog_titles_dataset.add(screenshot=event.image,
                                         screen_sample_matches=True,
                                         title_ocr=event.title_ocr,
                                         title_fuzzy_score=None,
                                         title_keys=event.title_keys)


class MapCalendarDatasetProcessor:
    NAME = MapCalendarsDataset.NAME
    @typechecked
    def __init__(self):
        from .MapScreen import map_screen_config
        from wa_screen_manager import config
        self.__logger = logging.getLogger(__name__)
        self.__map_calendars_dataset = MapCalendarsDataset(resolution=config.resolution,
                                                           crop=map_screen_config.map_calendar_box,
                                                           language=config.language)

    @typechecked
    def process(self, event: MapScreenEvent):
        self.__map_calendars_dataset.add(screenshot=event.image,
                                         calendar_ocr=event.calendar_ocr,
                                         calendar_overlapped=event.calendar_overlapped,
                                         date_key=event.date_timeofday.date_key
                                         if event.date_timeofday is not None else None,
                                         year=event.date_timeofday.year
                                         if event.date_timeofday is not None else None,
                                         day=event.date_timeofday.day
                                         if event.date_timeofday is not None else None,
                                         timeofday_key=event.date_timeofday.timeofday_key
                                         if event.date_timeofday is not None else None,)


class MasterDatasetsProcessor:
    @typechecked
    def __init__(self,
                 datasets: List[str],
                 player_name: Optional[str]):
        self.__dialog_relation_processor = (DialogRelationDatasetProcessor()
                                            if DialogRelationDatasetProcessor.NAME in datasets
                                            else None)
        self.__dialog_title_processor = (DialogTitleDatasetProcessor(player_name=player_name)
                                         if DialogTitleDatasetProcessor.NAME in datasets
                                         else None)
        self.__map_calendar_processor = (MapCalendarDatasetProcessor()
                                         if MapCalendarDatasetProcessor.NAME in datasets
                                         else None)

    @typechecked
    def on_dialog_screen(self, event: DialogScreenEvent):
        if self.__dialog_relation_processor:
            self.__dialog_relation_processor.process(event)
        if self.__dialog_title_processor:
            self.__dialog_title_processor.process(event)

    @typechecked
    def on_map_screen(self, event: MapScreenEvent):
        if self.__map_calendar_processor:
            self.__map_calendar_processor.process(event)
