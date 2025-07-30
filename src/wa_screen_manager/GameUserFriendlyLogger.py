import calendar as pycalendar
import logging

from wa_language.Language import Language
from wa_typechecker import typechecked

from wa_model import troop_keys
from wa_model import calendar_model
from wa_model.dialog_model.comment_intro_keys import (comment_intro_player_famous_checker,
                                                      comment_intro_player_noble_checker,
                                                      comment_intro_player_common_checker,
                                                      comment_intro_player_female_only_checker,
                                                      comment_intro_checker,
                                                      comment_intro_filter_by_lord_personality,
                                                      comment_intro_filter_king)
from wa_model.dialog_model.private_chat_keys import (is_private_chat_key,
                                                     private_chat_keys_by_lord_personality)
from .DialogScreen.DialogScreenEvent import DialogScreenEvent
from .MapScreen.MapScreenEvent import MapScreenEvent
from .GameScreenEvent import GameScreenEvent


class DialogScreenLogger:
    @typechecked
    def __init__(self, lang: Language):
        self.__logger = logging.getLogger(__name__)
        self.__lang = lang
        self.__eventHandlers = {
            DialogScreenEvent: self.on_dialog_screen,
            MapScreenEvent: self.on_map_screen
        }
        self.__prev_event_type = None
        self.__prev_map_date_timeofday = None
        self.__prev_dialog_title_ocr = None
        self.__prev_dialog_body_ocr = None
        self.__prev_dialog_relation = None

    @typechecked
    def on_game_screen_event(self, event: GameScreenEvent):
        if self.__prev_event_type != type(event):
            self.__prev_event_type = type(event)
            self.__logger.info(event.__class__.__name__.replace("ScreenEvent", " Screem"))
            self.clear_cache()
        event_handler = self.__eventHandlers.get(type(event))
        if event_handler:
            event_handler(event)

    @typechecked
    def clear_cache(self):
        self.__prev_map_date_timeofday = None
        self.__prev_dialog_title_ocr = None
        self.__prev_dialog_body_ocr = None
        self.__prev_dialog_relation = None

    @typechecked
    def on_map_screen(self, event: MapScreenEvent):
        if event.date_timeofday is None and event.calendar_overlapped:
            return
        if self.__prev_map_date_timeofday != event.date_timeofday:
            self.__prev_map_date_timeofday = event.date_timeofday
            text = "Map: "
            if event.date_timeofday:
                year = event.date_timeofday.year
                month = pycalendar.month_name[calendar_model.month(event.date_timeofday.date_key)]
                day = event.date_timeofday.day
                timeofday = self.__lang[event.date_timeofday.timeofday_key]
                text += f"{month[:3]} {day}, {year} - {timeofday}"
                if event.calendar_overlapped:
                    text += " (OVERLAPPED)"
            else:
                text += repr(event.calendar_ocr)
                text += " (FALSE NEGATIVE)"
            self.__logger.info(text)

    @typechecked
    def on_dialog_screen(self, event: DialogScreenEvent):
        # log title and body
        if (event.title_ocr is not None and
            event.body_ocr is not None and
                (event.body_ocr != self.__prev_dialog_body_ocr or
                 event.title_ocr != self.__prev_dialog_title_ocr)):
            self.__prev_dialog_body_ocr = event.body_ocr
            self.__prev_dialog_title_ocr = event.title_ocr
            self.__prev_dialog_relation = None
            # build title text
            text = "Dialog: "
            if event.title_keys:
                title_key = event.title_keys[0]
                val = self.__lang[title_key]
                if title_key in troop_keys.is_king_key:
                    text += f"Ruler {val}"
                elif title_key in troop_keys.is_lord_key:
                    text += f"Lord {val}"
                elif title_key in troop_keys.is_lady_key:
                    text += f"Lady {val}"
                else:
                    text += val
            else:
                text += repr(event.title_ocr_prep)
                text += " (FNE)"
            text += ": "
            # build body text
            if event.body_bounds:
                body_key = event.body_bounds[0].key
                if body_key in is_private_chat_key:
                    text += "Private chat"
                    for personality, checker in private_chat_keys_by_lord_personality.items():
                        if body_key in checker:
                            text += f" with {personality.value.capitalize()} lord"
                            break
                    text += f" ({body_key})"
                elif body_key in comment_intro_checker:
                    text += "Intro"
                    if body_key in comment_intro_filter_king:
                        text += " from King"
                    else:
                        for personality, checker in comment_intro_filter_by_lord_personality.items():
                            if body_key in checker:
                                text += f" from {personality.value.capitalize()} lord"
                                break
                    if body_key in comment_intro_player_common_checker:
                        text += " to Ordinary player"
                    elif body_key in comment_intro_player_noble_checker:
                        text += " to Noble player"
                    elif body_key in comment_intro_player_famous_checker:
                        text += " to Famous player"
                    elif body_key in comment_intro_player_female_only_checker:
                        text += " to Female"
                    text += f" ({body_key})"
            else:
                text += repr(event.body_ocr)
            self.__logger.info(text)
        # log relation
        if (
            event.relation_ocr is not None and
            event.title_ocr is not None and
            event.body_ocr is not None and
            event.body_ocr == self.__prev_dialog_body_ocr and
            event.title_ocr == self.__prev_dialog_title_ocr and
            event.relation != self.__prev_dialog_relation
        ):
            self.__prev_dialog_relation = event.relation
            text = " "*len("Dialog: ")
            text += "Relation: " + str(event.relation) if event.relation is not None else "?"
            self.__logger.info(text)
