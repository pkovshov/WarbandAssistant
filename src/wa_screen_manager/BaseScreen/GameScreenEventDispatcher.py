from typing import Callable

from typeguard import typechecked

from ..GameScreenEvent import GameScreenEvent


class GameScreenEventDispatcher:
    def __init__(self):
        self.__handlers = []

    @typechecked
    def append_handler(self, handler: Callable[[GameScreenEvent], None]):
        if handler not in self.__handlers:
            self.__handlers.append(handler)

    @typechecked
    def _dispatch(self, event: GameScreenEvent):
        for handler in self.__handlers:
            handler(event)
