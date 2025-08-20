import logging
from os import path
from typing import Optional, List

from wa_typechecker import typechecked

import path_conf
from wa_types import LanguageCode
from wa_language.LangVar import PlayerSex
from wa_datasets.DialogBodiesDataset import DialogBodiesDataset
from wa_datasets.DialogRelationsDataset import DialogRelationsDataset
from wa_datasets.DialogTitlesDataset import DialogTitlesDataset
from wa_datasets.MapCalendarsDataset import MapCalendarsDataset
from .DialogScreen.DialogScreenEvent import DialogScreenEvent
from .MapScreen.MapScreenEvent import MapScreenEvent
from .GameScreenEvent import GameScreenEvent


class DialogBodyProcessor:
    NAME = DialogBodiesDataset.NAME
    @typechecked
    def __init__(self,
                 language_code: LanguageCode,
                 player_name: Optional[str],
                 player_sex: Optional[PlayerSex]):
        from .DialogScreen import dialog_screen_config
        from wa_screen_manager import config
        self.__dataset = DialogBodiesDataset(resolution=config.resolution,
                                             crop=dialog_screen_config.body_box,
                                             language=str(language_code),
                                             player_name=player_name,
                                             player_sex=player_sex,
                                             blank_img_path=path.join(path_conf.samples,
                                                                      dialog_screen_config.dialog_screen_blank_img_path))
        self.__prev_body_ocr = None

    @typechecked
    def on_game_screen_event(self, event: GameScreenEvent):
        if isinstance(event, DialogScreenEvent):
            if event.body_ocr is not None and event.body_ocr != self.__prev_body_ocr:
                self.__prev_body_ocr = event.body_ocr
                self.__dataset.add(screenshot=event.image,
                                   screen_sample_matches=True,
                                   title_keys=event.title_keys,
                                   body_ocr=event.body_ocr,
                                   body_bounds=event.body_bounds)
        else:
            self.__prev_body_ocr = None

class DialogRelationDatasetProcessor:
    NAME = DialogRelationsDataset.NAME
    @typechecked
    def __init__(self,
                 language_code: LanguageCode):
        from .DialogScreen import dialog_screen_config
        from wa_screen_manager import config
        self.__dialog_relations_dataset = DialogRelationsDataset(resolution=config.resolution,
                                                                 crop=dialog_screen_config.relation_box,
                                                                 language=str(language_code))

    @typechecked
    def on_game_screen_event(self, event: GameScreenEvent):
        if isinstance(event, DialogScreenEvent):
            if event.relation_ocr is not None:
                self.__dialog_relations_dataset.add(screenshot=event.image,
                                                    screen_sample_matches=True,
                                                    relation_ocr=event.relation_ocr,
                                                    relation=event.relation)


class DialogTitleDatasetProcessor:
    NAME = DialogTitlesDataset.NAME
    @typechecked
    def __init__(self,
                 language_code: LanguageCode,
                 player_name: Optional[str]):
        from .DialogScreen import dialog_screen_config
        from wa_screen_manager import config
        self.__dialog_titles_dataset = DialogTitlesDataset(resolution=config.resolution,
                                                           crop=dialog_screen_config.title_box,
                                                           language=str(language_code),
                                                           player_name=player_name)
        self.__prev_title_ocr = None

    @typechecked
    def on_game_screen_event(self, event: GameScreenEvent):
        if isinstance(event, DialogScreenEvent):
            if self.__prev_title_ocr != event.title_ocr:
                self.__prev_title_ocr = event.title_ocr
                self.__dialog_titles_dataset.add(screenshot=event.image,
                                                 screen_sample_matches=True,
                                                 title_ocr=event.title_ocr,
                                                 title_fuzzy_score=None,
                                                 title_keys=event.title_keys)
        else:
            self.__prev_title_ocr = None


class MapCalendarDatasetProcessor:
    NAME = MapCalendarsDataset.NAME
    @typechecked
    def __init__(self,
                 language_code: LanguageCode):
        from .MapScreen import map_screen_config
        from wa_screen_manager import config
        self.__logger = logging.getLogger(__name__)
        self.__map_calendars_dataset = MapCalendarsDataset(resolution=config.resolution,
                                                           crop=map_screen_config.map_calendar_box,
                                                           language=str(language_code))

    @typechecked
    def on_game_screen_event(self, event: GameScreenEvent):
        if isinstance(event, MapScreenEvent):
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
                 language_code: LanguageCode,
                 player_name: Optional[str],
                 player_sex: Optional[PlayerSex]):
        self.__dialog_body_processor = (DialogBodyProcessor(language_code=language_code,
                                                            player_name=player_name,
                                                            player_sex=player_sex)
                                        if DialogBodyProcessor.NAME in datasets
                                        else None)
        self.__dialog_relation_processor = (DialogRelationDatasetProcessor(language_code=language_code,)
                                            if DialogRelationDatasetProcessor.NAME in datasets
                                            else None)
        self.__dialog_title_processor = (DialogTitleDatasetProcessor(language_code=language_code,
                                                                     player_name=player_name)
                                         if DialogTitleDatasetProcessor.NAME in datasets
                                         else None)
        self.__map_calendar_processor = (MapCalendarDatasetProcessor(language_code=language_code,)
                                         if MapCalendarDatasetProcessor.NAME in datasets
                                         else None)

    def on_game_screen_event(self, event: GameScreenEvent):
        if self.__dialog_body_processor:
            self.__dialog_body_processor.on_game_screen_event(event)
        if self.__dialog_relation_processor:
            self.__dialog_relation_processor.on_game_screen_event(event)
        if self.__dialog_title_processor:
            self.__dialog_title_processor.on_game_screen_event(event)
        if self.__map_calendar_processor:
            self.__map_calendar_processor.on_game_screen_event(event)
