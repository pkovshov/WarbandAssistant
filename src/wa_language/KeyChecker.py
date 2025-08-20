"""
Tests:
>>> from wa_types import LanguageCode
>>> from wa_language.Language import RootLanguage
>>> lang = RootLanguage(dict(a="Anna", b="Boris", good="Robin Hood", bad="Ursula", fool="Pippin Took"),
...                     language_code=LanguageCode.EN)

>>> is_alphabet = key_checker("alpha", "beta", "gama")
>>> LangKey("alpha") in is_alphabet
True
>>> LangKey("alpha") in is_alphabet.lang(lang)
False

>>> is_hero = KeyChecker(lambda key: key in ("good", "bad", "fool"))
>>> LangKey("dom") in is_hero
False
>>> LangKey("good") in is_hero
True
>>> print(*sorted(is_hero.lang(lang).values()), sep=", ")
Pippin Took, Robin Hood, Ursula

>>> is_good = KeyChecker("good")
>>> LangKey("good") in is_good
True
>>> LangKey("bad") in is_good
False
>>> print(*is_good.lang(lang).values(), sep=", ")
Robin Hood
>>> is_good == is_hero
False
>>> hash(is_good) == hash(is_hero)  # Might be True for hash collision case
False

>>> is_good_2 = KeyChecker("good")
>>> is_good_2 is is_good
False
>>> set(is_good_2.lang(lang).values()) == set(is_good.lang(lang).values())
True
>>> is_good_2 == is_good
True
>>> hash(is_good_2) == hash(is_good)
True

>>> is_hero_mult = KeyChecker(["good", "bad", "fool"])
>>> LangKey("dom") in is_hero_mult
False
>>> LangKey("good") in is_hero_mult
True
>>> print(*sorted(is_hero_mult.lang(lang).values()), sep=", ")
Pippin Took, Robin Hood, Ursula
>>> set(is_hero_mult.lang(lang).values()) == set(is_hero.lang(lang).values())
True
>>> is_hero_mult == is_hero
False
>>> hash(is_hero_mult) == hash(is_hero)  # Might be True for hash collision case
False

>>> is_hero_mult_2 = KeyChecker("good", "bad", "fool")
>>> LangKey("dom") in is_hero_mult_2
False
>>> LangKey("good") in is_hero_mult_2
True
>>> print(*sorted(is_hero_mult_2.lang(lang).values()), sep=", ")
Pippin Took, Robin Hood, Ursula
>>> is_hero_mult_2 is is_hero_mult
False
>>> set(is_hero_mult_2.lang(lang).values()) == set(is_hero_mult.lang(lang).values())
True
>>> is_hero_mult_2 == is_hero_mult
True
>>> hash(is_hero_mult_2) == hash(is_hero_mult)
True

>>> is_hero_mult_3 = KeyChecker(is_good, "bad", lambda x: x=="fool")
>>> LangKey("dom") in is_hero_mult_3
False
>>> LangKey("good") in is_hero_mult_3
True
>>> print(*sorted(is_hero_mult_3.lang(lang).values()), sep=", ")
Pippin Took, Robin Hood, Ursula
>>> is_hero_mult_3 is is_hero_mult
False
>>> is_hero_mult_3.lang(lang) is is_hero_mult.lang(lang)
False
>>> dict(is_hero_mult_3.lang(lang)) == dict(is_hero_mult.lang(lang))
True
>>> set(is_hero_mult_3.lang(lang).values()) == set(is_hero_mult.lang(lang).values())
True
>>> is_hero_mult_3 == is_hero_mult  # due to lambda
False
>>> hash(is_hero_mult_3) == hash(is_hero_mult)  # due to lambda
False

>>> is_hero_mult_4 = KeyChecker((lambda val: val == "good"), "bad", "fool")
>>> LangKey("dom") in is_hero_mult_4
False
>>> LangKey("good") in is_hero_mult_4
True
>>> print(*sorted(is_hero_mult_4.lang(lang).values()), sep=", ")
Pippin Took, Robin Hood, Ursula
>>> set(is_hero_mult_4.lang(lang).values()) == set(is_hero_mult.lang(lang).values())
True
>>> is_hero_mult_4 == is_hero_mult  # due to KeyChecker("good") != KeyChecker(lambda val: val == "good")
False
>>> hash(is_hero_mult_4) == hash(is_hero_mult)  # Might be True for hash collision case
False

>>> KeyChecker("good") == KeyChecker(lambda val: val == "good")
False
>>> dict(KeyChecker("good").lang(lang)) == dict(KeyChecker(lambda val: val == "good").lang(lang))
True

>>> is_good_mult = KeyChecker(KeyChecker(KeyChecker("good")))
>>> LangKey("good") in is_good_mult
True
>>> is_good_mult is is_good
False
>>> set(is_good_mult.lang(lang).values()) == set(is_good_mult.lang(lang).values())
True
>>> is_good_mult == is_good
True
>>> hash(is_good_mult) == hash(is_good)
True

>>> is_not_good_hero = KeyChecker(is_hero, deny_filter=is_good)
>>> LangKey("bad") in is_not_good_hero
True
>>> LangKey("fool") in is_not_good_hero
True
>>> LangKey("good") in is_not_good_hero
False
>>> print(*sorted(is_not_good_hero.lang(lang).values()), sep=", ")
Pippin Took, Ursula
>>> KeyChecker(is_not_good_hero) is is_not_good_hero
True
>>> is_not_good_hero_same = KeyChecker(is_hero, deny_filter=is_good)
>>> is_not_good_hero_same is is_not_good_hero
False
>>> set(is_not_good_hero_same.lang(lang).values()) == set(is_not_good_hero.lang(lang).values())
True
>>> is_not_good_hero_same == is_not_good_hero
True
>>> hash(is_not_good_hero_same) == hash(is_not_good_hero)
True

>>> is_oo_hero = KeyChecker(is_hero, pass_filter=KeyChecker(lambda x: "oo" in x))
>>> LangKey("bad") in is_oo_hero
False
>>> LangKey("fool") in is_oo_hero
True
>>> LangKey("good") in is_oo_hero
True
>>> print(*sorted(is_oo_hero.lang(lang).values()), sep=", ")
Pippin Took, Robin Hood
>>> KeyChecker(is_oo_hero) is is_oo_hero
True
>>> is_oo_hero_same = KeyChecker(is_hero, pass_filter=KeyChecker(lambda x: "oo" in x))
>>> is_oo_hero_same is is_oo_hero
False
>>> set(is_oo_hero_same.lang(lang).values()) == set(is_oo_hero.lang(lang).values())
True
>>> is_oo_hero_same == is_oo_hero  # due to same labda functions are not equal
False
>>> hash(is_oo_hero_same) == hash(is_oo_hero)  # due to same labda functions are not equal
False

>>> is_not_good_fool_hero = KeyChecker(is_hero, deny_filter=is_good, pass_filter=KeyChecker("fool"))
>>> LangKey("bad") in is_not_good_fool_hero
False
>>> LangKey("fool") in is_not_good_fool_hero
True
>>> LangKey("good") in is_not_good_fool_hero
False
>>> print(*is_not_good_fool_hero.lang(lang).values(), sep=", ")
Pippin Took
>>> KeyChecker(is_not_good_fool_hero) is is_not_good_fool_hero
True
>>> is_not_good_fool_hero_same = KeyChecker(is_hero, deny_filter=is_good, pass_filter=KeyChecker("fool"))
>>> is_not_good_fool_hero_same is is_not_good_fool_hero
False
>>> set(is_not_good_fool_hero_same.lang(lang).values()) == set(is_not_good_fool_hero.lang(lang).values())
True
>>> is_not_good_fool_hero_same == is_not_good_fool_hero
True
>>> hash(is_not_good_fool_hero_same) == hash(is_not_good_fool_hero)
True

>>> KeyChecker(1)
Traceback (most recent call last):
TypeError: ...
>>> KeyChecker([1, 2, 3])
Traceback (most recent call last):
TypeError: ...
>>> KeyChecker(1, 2, 3)
Traceback (most recent call last):
TypeError: ...
>>> KeyChecker("good", ["bad", "some"])
Traceback (most recent call last):
TypeError: ...
>>> print(*KeyChecker("good", KeyChecker("bad", "some")).lang(lang).values(), sep=', ')
Robin Hood, Ursula

>>> is_hero.lang(lang) is is_hero.lang(lang)
True
"""

from typing import Callable, Iterable, Optional

from wa_typechecker import typechecked
from .Language import Language
from .LangKey import LangKey


class KeyChecker:
    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], KeyChecker):
            return args[0]
        else:
            return super().__new__(cls)

    @typechecked
    def __init__(self, *args,
                 pass_filter: Optional["KeyChecker"] = None,
                 deny_filter: Optional["KeyChecker"] = None):
        if len(args) == 1 and args[0] is self:
            return  # do nothing to avoid maximum recursion depth exceeded
        self.__lang = None
        self.__pass_filter = pass_filter
        self.__deny_filter = deny_filter
        checkers = []
        if len(args) == 0:
            self.__check = None
            return
        if len(args) == 1:
            checker = args[0]
            if isinstance(checker, str):
                self.__str = checker
                self.__check = self.__check_str
                return
            elif isinstance(checker, KeyChecker):
                self.__checkers = checker,
                self.__check = self.__check_tuple
                return
            elif isinstance(checker, Callable):
                self.__check = checker
                return
            elif isinstance(checker, Iterable):
                checkers.extend(KeyChecker(checker) for checker in checker)
            else:
                raise TypeError(f"KeyChecker expected str or callable or iterable, got {repr(checker)}")
        else:
            for arg in args:
                if isinstance(arg, KeyChecker):
                    checkers.append(arg)
                elif isinstance(arg, str):
                    checkers.append(KeyChecker(arg))
                elif isinstance(arg, Callable):
                    checkers.append(KeyChecker(arg))
                else:
                    raise TypeError(f"KeyChecker expected str or callable, got {repr(arg)}")
        self.__checkers = tuple(checkers)
        self.__check = self.__check_tuple

    def __check_str(self, lang_key):
        return self.__str == lang_key

    def __check_tuple(self, lang_key) -> bool:
        return any(lang_key in checker for checker in self.__checkers)

    def __contains__(self, lang_key) -> bool:
        return ((lang_key in self.__pass_filter if self.__pass_filter else True) and
                (lang_key not in self.__deny_filter if self.__deny_filter else True) and
                (self.__check(lang_key) if self.__check else True))

    @typechecked
    def lang(self, language: Language) -> Language:
        if language is not self.__lang:
            self.__lang = language
            self.__lang_key_checker = KeyCheckerLanguage(language, self)
        return self.__lang_key_checker

    @typechecked
    def __call__(self, lang: Language) -> Language:
        # deprecated
        raise NotImplementedError()
        if lang is not self.__lang:
            self.__lang = lang
            self.__lang_key_checker = KeyCheckerLanguage(lang, self)
        return self.__lang_key_checker

    def __eq__(self, other):
        if not isinstance(other, KeyChecker):
            return NotImplemented
        if self.__pass_filter != other.__pass_filter:
            return False
        if self.__deny_filter != other.__deny_filter:
            return False
        try:
            return self.__str == other.__str
        except AttributeError:
            try:
                return self.__checkers == other.__checkers
            except AttributeError:
                return self.__check == other.__check

    def __hash__(self):
        filter_and_exclude = self.__pass_filter, self.__deny_filter
        try:
            return hash((self.__str, filter_and_exclude))
        except AttributeError:
            try:
                return hash((self.__checkers, filter_and_exclude))
            except AttributeError:
                return hash((self.__check, filter_and_exclude))


class KeyCheckerLanguage(Language):
    @typechecked
    def __init__(self, lang: Language, checker: KeyChecker):
        super().__init__({key: val
                          for key, val in lang.items()
                          if key in checker},
                         language_code=lang.language_code)


def key_checker(*args, pass_filter=None, deny_filter=None):
    return KeyChecker(*args, pass_filter=pass_filter, deny_filter=deny_filter)
