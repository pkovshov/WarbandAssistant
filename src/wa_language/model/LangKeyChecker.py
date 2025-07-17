"""
Tests:
>>> lang = Language(dict(a="Anna", b="Boris", good="Robin Hood", bad="Ursula", fool="Pippin Took"))

>>> is_alphabet = key_checker("alpha", "beta", "gama")
>>> LangKey("alpha") in is_alphabet
True
>>> LangKey("alpha") in is_alphabet(lang)
False

>>> is_hero = KeyChecker(lambda key: key in ("good", "bad", "fool"))
>>> "dom" in is_hero
Traceback (most recent call last):
typeguard.TypeCheckError: ...
>>> LangKey("dom") in is_hero
False
>>> LangKey("good") in is_hero
True
>>> print(*sorted(is_hero(lang).values()), sep=", ")
Pippin Took, Robin Hood, Ursula

>>> is_good = KeyChecker("good")
>>> LangKey("good") in is_good
True
>>> LangKey("bad") in is_good
False
>>> print(*is_good(lang).values(), sep=", ")
Robin Hood
>>> is_good == is_hero
False
>>> hash(is_good) == hash(is_hero)  # Might be True for hash collision case
False

>>> is_good_2 = KeyChecker("good")
>>> is_good_2 is is_good
False
>>> set(is_good_2(lang).values()) == set(is_good(lang).values())
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
>>> print(*sorted(is_hero_mult(lang).values()), sep=", ")
Pippin Took, Robin Hood, Ursula
>>> set(is_hero_mult(lang).values()) == set(is_hero(lang).values())
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
>>> print(*sorted(is_hero_mult_2(lang).values()), sep=", ")
Pippin Took, Robin Hood, Ursula
>>> is_hero_mult_2 is is_hero_mult
False
>>> set(is_hero_mult_2(lang).values()) == set(is_hero_mult(lang).values())
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
>>> print(*sorted(is_hero_mult_3(lang).values()), sep=", ")
Pippin Took, Robin Hood, Ursula
>>> is_hero_mult_3 is is_hero_mult
False
>>> is_hero_mult_3(lang) is is_hero_mult(lang)
False
>>> is_hero_mult_3(lang) == is_hero_mult(lang)
True
>>> set(is_hero_mult_3(lang).values()) == set(is_hero_mult(lang).values())
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
>>> print(*sorted(is_hero_mult_4(lang).values()), sep=", ")
Pippin Took, Robin Hood, Ursula
>>> set(is_hero_mult_4(lang).values()) == set(is_hero_mult(lang).values())
True
>>> is_hero_mult_4 == is_hero_mult  # due to KeyChecker("good") != KeyChecker(lambda val: val == "good")
False
>>> hash(is_hero_mult_4) == hash(is_hero_mult)  # Might be True for hash collision case
False

>>> KeyChecker("good") == KeyChecker(lambda val: val == "good")
False
>>> KeyChecker("good")(lang) == KeyChecker(lambda val: val == "good")(lang)
True

>>> is_good_mult = KeyChecker(KeyChecker(KeyChecker("good")))
>>> LangKey("good") in is_good_mult
True
>>> is_good_mult is is_good
False
>>> set(is_good_mult(lang).values()) == set(is_good_mult(lang).values())
True
>>> is_good_mult == is_good
True
>>> hash(is_good_mult) == hash(is_good)
True

>>> is_not_good_hero = KeyChecker(is_hero, exclude=is_good)
>>> LangKey("bad") in is_not_good_hero
True
>>> LangKey("fool") in is_not_good_hero
True
>>> LangKey("good") in is_not_good_hero
False
>>> print(*sorted(is_not_good_hero(lang).values()), sep=", ")
Pippin Took, Ursula
>>> KeyChecker(is_not_good_hero) is is_not_good_hero
True
>>> is_not_good_hero_same = KeyChecker(is_hero, exclude=is_good)
>>> is_not_good_hero_same is is_not_good_hero
False
>>> set(is_not_good_hero_same(lang).values()) == set(is_not_good_hero(lang).values())
True
>>> is_not_good_hero_same == is_not_good_hero
True
>>> hash(is_not_good_hero_same) == hash(is_not_good_hero)
True

>>> is_oo_hero = KeyChecker(is_hero, filter=KeyChecker(lambda x: "oo" in x))
>>> LangKey("bad") in is_oo_hero
False
>>> LangKey("fool") in is_oo_hero
True
>>> LangKey("good") in is_oo_hero
True
>>> print(*sorted(is_oo_hero(lang).values()), sep=", ")
Pippin Took, Robin Hood
>>> KeyChecker(is_oo_hero) is is_oo_hero
True
>>> is_oo_hero_same = KeyChecker(is_hero, filter=KeyChecker(lambda x: "oo" in x))
>>> is_oo_hero_same is is_oo_hero
False
>>> set(is_oo_hero_same(lang).values()) == set(is_oo_hero(lang).values())
True
>>> is_oo_hero_same == is_oo_hero  # due to same labda functions are not equal
False
>>> hash(is_oo_hero_same) == hash(is_oo_hero)  # due to same labda functions are not equal
False

>>> is_not_good_fool_hero = KeyChecker(is_hero, exclude=is_good, filter=KeyChecker("fool"))
>>> LangKey("bad") in is_not_good_fool_hero
False
>>> LangKey("fool") in is_not_good_fool_hero
True
>>> LangKey("good") in is_not_good_fool_hero
False
>>> print(*is_not_good_fool_hero(lang).values(), sep=", ")
Pippin Took
>>> KeyChecker(is_not_good_fool_hero) is is_not_good_fool_hero
True
>>> is_not_good_fool_hero_same = KeyChecker(is_hero, exclude=is_good, filter=KeyChecker("fool"))
>>> is_not_good_fool_hero_same is is_not_good_fool_hero
False
>>> set(is_not_good_fool_hero_same(lang).values()) == set(is_not_good_fool_hero(lang).values())
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
>>> print(*KeyChecker("good", KeyChecker("bad", "some"))(lang).values(), sep=', ')
Robin Hood, Ursula

>>> is_hero(lang) is is_hero(lang)
True
"""

from typing import Callable, Iterable, Iterator, Mapping, Optional

from typeguard import typechecked

from wa_language.Language import Language, LangKey, LangValue


class KeyChecker:
    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], KeyChecker):
            return args[0]
        else:
            return super().__new__(cls)

    @typechecked
    def __init__(self, *args, filter: Optional["KeyChecker"] = None, exclude: Optional["KeyChecker"] = None):
        if len(args) == 1 and args[0] is self:
            return  # do nothing to avoid maximum recursion depth exceeded
        self.__lang = None
        self.__filter = filter
        self.__exclude = exclude
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

    def __check_str(self, val):
        return self.__str == val

    def __check_tuple(self, key: LangKey) -> bool:
        return any(key in checker for checker in self.__checkers)

    @typechecked
    def __contains__(self, key: LangKey) -> bool:
        return ((key in self.__filter if self.__filter else True) and
                (key not in self.__exclude if self.__exclude else True) and
                (self.__check(key) if self.__check else True))

    @typechecked
    def lang(self, language: Language) -> "LangKeyChecker":
        if language is not self.__lang:
            self.__lang = language
            self.__lang_key_checker = LangKeyChecker(language, self)
        return self.__lang_key_checker

    @typechecked
    def __call__(self, lang: Language) -> "LangKeyChecker":
        if lang is not self.__lang:
            self.__lang = lang
            self.__lang_key_checker = LangKeyChecker(lang, self)
        return self.__lang_key_checker

    def __eq__(self, other):
        if not isinstance(other, KeyChecker):
            return NotImplemented
        if self.__filter != other.__filter:
            return False
        if self.__exclude != other.__exclude:
            return False
        try:
            return self.__str == other.__str
        except AttributeError:
            try:
                return self.__checkers == other.__checkers
            except AttributeError:
                return self.__check == other.__check

    def __hash__(self):
        filter_and_exclude = self.__filter, self.__exclude
        try:
            return hash((self.__str, filter_and_exclude))
        except AttributeError:
            try:
                return hash((self.__checkers, filter_and_exclude))
            except AttributeError:
                return hash((self.__check, filter_and_exclude))


class LangKeyChecker(Mapping[LangKey, LangValue]):
    @typechecked
    def __init__(self, lang: Language, checker: KeyChecker):
        self.__data = {key: val for key, val in lang.items() if key in checker}

    @typechecked
    def __getitem__(self, key: LangKey) -> LangValue:
        return self.__data[key]

    def __iter__(self) -> Iterator[LangKey]:
        return iter(self.__data)

    @typechecked
    def __contains__(self, key: LangKey) -> bool:
        return key in self.__data

    def __len__(self) -> int:
        return len(self.__data)


def key_checker(*args, filter=None, exclude=None):
    return KeyChecker(*args, filter=filter, exclude=exclude)
