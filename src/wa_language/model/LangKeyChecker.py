"""
Tests:
>>> lang = Language(dict(a="Anna", b="Boris", good="Robin Hood", bad="Ursula"))

>>> is_hero = LangKeyChecker(lambda key: key in ("good", "bad"))
>>> is_hero("dom")
Traceback (most recent call last):
typeguard.TypeCheckError: ...
>>> is_hero(LangKey("dom"))
False
>>> is_hero(LangKey("good"))
True
>>> print(*is_hero.values(lang), sep=", ")
Robin Hood, Ursula

>>> is_good = LangKeyChecker("good")
>>> is_good(LangKey("good"))
True
>>> is_good(LangKey("bad"))
False
>>> print(*is_good.values(lang), sep=", ")
Robin Hood
>>> is_good == is_hero
False
>>> hash(is_good) == hash(is_hero)  # Might be True for hash collision case
False

>>> is_good_2 = LangKeyChecker("good")
>>> is_good_2 is is_good
False
>>> is_good_2.values(lang) == is_good.values(lang)
True
>>> is_good_2 == is_good
True
>>> hash(is_good_2) == hash(is_good)
True

>>> is_hero_mult = LangKeyChecker(["good", "bad"])
>>> is_hero_mult(LangKey("dom"))
False
>>> is_hero_mult(LangKey("good"))
True
>>> print(*is_hero_mult.values(lang), sep=", ")
Robin Hood, Ursula
>>> is_hero_mult.values(lang) == is_hero.values(lang)
True
>>> is_hero_mult == is_hero
False
>>> hash(is_hero_mult) == hash(is_hero)  # Might be True for hash collision case
False

>>> is_hero_mult_2 = LangKeyChecker("good", "bad")
>>> is_hero_mult_2(LangKey("dom"))
False
>>> is_hero_mult_2(LangKey("good"))
True
>>> print(*is_hero_mult_2.values(lang), sep=", ")
Robin Hood, Ursula
>>> is_hero_mult_2 is is_hero_mult
False
>>> is_hero_mult_2.values(lang) == is_hero_mult.values(lang)
True
>>> is_hero_mult_2 == is_hero_mult
True
>>> hash(is_hero_mult_2) == hash(is_hero_mult)
True

>>> is_hero_mult_3 = LangKeyChecker(is_good, "bad")
>>> is_hero_mult_3(LangKey("dom"))
False
>>> is_hero_mult_3(LangKey("good"))
True
>>> print(*is_hero_mult_3.values(lang), sep=", ")
Robin Hood, Ursula
>>> is_hero_mult_3 is is_hero_mult
False
>>> is_hero_mult_3.values(lang) == is_hero_mult.values(lang)
True
>>> is_hero_mult_3 == is_hero_mult
True
>>> hash(is_hero_mult_3) == hash(is_hero_mult)
True

>>> is_hero_mult_4 = LangKeyChecker((lambda val: val == "good"), "bad")
>>> is_hero_mult_4(LangKey("dom"))
False
>>> is_hero_mult_4(LangKey("good"))
True
>>> print(*is_hero_mult_4.values(lang), sep=", ")
Robin Hood, Ursula
>>> is_hero_mult_4.values(lang) == is_hero_mult.values(lang)
True
>>> is_hero_mult_4 == is_hero_mult  # due to LangKeyChecker("good") != LangKeyChecker(lambda val: val == "good")
False
>>> hash(is_hero_mult_4) == hash(is_hero_mult)  # Might be True for hash collision case
False

>>> LangKeyChecker("good") == LangKeyChecker(lambda val: val == "good")
False
>>> LangKeyChecker("good")(LangKey("good")) == LangKeyChecker(lambda val: val == "good")(LangKey("good"))
True
>>> LangKeyChecker("good")(LangKey("Vaiop")) == LangKeyChecker(lambda val: val == "good")(LangKey("Pejik"))
True

>>> is_good_mult = LangKeyChecker(LangKeyChecker(LangKeyChecker("good")))
>>> is_good_mult(LangKey("good"))
True
>>> is_good_mult is is_good
False
>>> is_good_mult.values(lang) == is_good_mult.values(lang)
True
>>> is_good_mult == is_good
True
>>> hash(is_good_mult) == hash(is_good)
True

>>> LangKeyChecker(1)
Traceback (most recent call last):
TypeError: ...
>>> LangKeyChecker([1, 2, 3])
Traceback (most recent call last):
TypeError: ...
>>> LangKeyChecker(1, 2, 3)
Traceback (most recent call last):
TypeError: ...
>>> LangKeyChecker("good", ["bad", "some"])
Traceback (most recent call last):
TypeError: ...
>>> print(*LangKeyChecker("good", LangKeyChecker("bad", "some")).values(lang), sep=', ')
Robin Hood, Ursula
"""

from typing import Callable, Iterable, Tuple

from typeguard import typechecked

from wa_language.Language import Language, LangKey, LangValue


class LangKeyChecker:
    def __new__(cls, *args):
        if len(args) == 1 and isinstance(args[0], LangKeyChecker):
            return args[0]
        else:
            return super().__new__(cls)

    def __init__(self, *args):
        if len(args) == 0:
            raise TypeError("LangKeyChecker expected at least 1 argument, got 0")
        self.__lang = None
        self.__values = None
        checkers = []
        if len(args) == 1:
            checker = args[0]
            if checker is self:
                return  # do nothing to avoid maximum recursion depth exceeded
            elif isinstance(checker, str):
                self.__str = checker
                self.__check = self.__check_str
                return
            elif isinstance(checker, Callable):
                self.__check = checker
                return
            elif isinstance(checker, Iterable):
                checkers.extend(LangKeyChecker(checker) for checker in checker)
            else:
                raise TypeError(f"LangKeyChecker expected str or callable or iterable, got {repr(checker)}")
        else:
            for arg in args:
                if isinstance(arg, LangKeyChecker):
                    checkers.append(arg)
                elif isinstance(arg, str):
                    checkers.append(LangKeyChecker(arg))
                elif isinstance(arg, Callable):
                    checkers.append(LangKeyChecker(arg))
                else:
                    raise TypeError(f"LangKeyChecker expected str or callable, got {repr(arg)}")
        self.__checkers = tuple(checkers)
        self.__check = self.__check_tuple

    def __check_str(self, val):
        return self.__str == val

    def __check_tuple(self, key: LangKey) -> bool:
        return any(checker(key) for checker in self.__checkers)

    @typechecked
    def __call__(self, key: LangKey) -> bool:
        return self.__check(key)

    def __eq__(self, other):
        if not isinstance(other, LangKeyChecker):
            return NotImplemented
        try:
            return self.__str == other.__str
        except AttributeError:
            try:
                return self.__checkers == other.__checkers
            except AttributeError:
                return self.__check == other.__check

    def __hash__(self):
        try:
            return hash(self.__str)
        except AttributeError:
            try:
                return hash(self.__checkers)
            except AttributeError:
                return hash(self.__check)

    @typechecked
    def values(self, lang: Language) -> Tuple[LangValue, ...]:
        if lang != self.__lang:
            self.__lang = lang
            self.__values = tuple(val for key, val in lang.items() if self(key))
        return self.__values


def key_checker(*args) -> LangKeyChecker:
    return LangKeyChecker(*args)
