from typing import Callable, Tuple

from typeguard import typechecked

from wa_language.Language import Language, LangKey, LangValue


class KeyChecker:
    """
    Tests:
    >>> is_hero = KeyChecker(lambda key: key in ("good", "bad"))
    >>> is_hero("dom")
    Traceback (most recent call last):
    typeguard.TypeCheckError: ...
    >>> is_hero(LangKey("dom"))
    False
    >>> is_hero(LangKey("good"))
    True
    >>> lang = Language(dict(a="Anna", b="Boris", good="Robin Hood", bad="Ursula"))
    >>> print(*is_hero.values(lang), sep=", ")
    Robin Hood, Ursula
    """
    @typechecked
    def __init__(self, check: Callable[[LangKey], bool]):
        self.__check = check
        self.__lang = None
        self.__values = None

    @typechecked
    def __call__(self, key: LangKey) -> bool:
        return self.__check(key)

    @typechecked
    def values(self, lang: Language) -> Tuple[LangValue, ...]:
        if lang != self.__lang:
            self.__lang = lang
            self.__values = tuple(val for key, val in lang.items() if self(key))
        return self.__values


def key_checker(func: Callable[[LangKey], bool]) -> KeyChecker:
    return KeyChecker(func)


class MultiKeyChecker(KeyChecker):
    @typechecked
    def __init__(self, checkers: Tuple[KeyChecker, ...]):
        self.__checkers = checkers
        super().__init__(self.__check)

    def __check(self, key: LangKey) -> bool:
        return any(checker(key) for checker in self.__checkers)
