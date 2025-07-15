import calendar as pycalendar
import logging
from typing import Callable, Mapping

from wa_language import LangValParser
from typeguard import typechecked

from wa_language.model import troop_keys
from wa_language.model import calendar_model
from wa_screen_manager.DialogScreen.DialogScreenEvent import DialogScreenEvent
from wa_screen_manager.MapScreen.MapScreenEvent import MapScreenEvent


class DialogScreenLogger:
    @typechecked
    def __init__(self, lang: Mapping[str, LangValParser.Interpolation]):
        self.__logger = logging.getLogger(__name__)
        self.__lang = lang
        self.__listener = None
        self.__prev_date_timeofday = None

    @property
    def listener(self):
        return self.__listener

    @listener.setter
    @typechecked
    def listener(self, value: Callable[[str], None]):
        self.__listener = value

    def on_unknown_screen(self):
        self.__prev_date_timeofday = None

    @typechecked
    def on_map_screen(self, event: MapScreenEvent):
        if event.date_timeofday is None and event.calendar_overlapped:
            return
        if self.__prev_date_timeofday != event.date_timeofday:
            self.__prev_date_timeofday = event.date_timeofday
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
            if self.__listener:
                self.__listener(text)
            else:
                self.__logger.info(text)

    @typechecked
    def on_dialog_screen(self, event: DialogScreenEvent):
        text = "Dialog: "
        if event.title_keys:
            title_key = event.title_keys[0]
            val = self.__lang[title_key]
            if troop_keys.is_king_key(title_key):
                text += f"Ruler {val}"
            elif troop_keys.is_lord_key(title_key):
                text += f"Lord {val}"
            elif troop_keys.is_lady_key(title_key):
                text += f"Lady {val}"
            else:
                text += val
        else:
            text += repr(event.title)
        if event.relation_ocr is not None:
            text += " "
            text += str(event.relation) if event.relation is not None else "?"
        if not event.title_keys:
            text += " (FALSE NEGATIVE)"
        if self.__listener:
            self.__listener(text)
        else:
            self.__logger.info(text)
