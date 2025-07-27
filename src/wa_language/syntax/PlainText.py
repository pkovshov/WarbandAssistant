"""
Tests:
>>> PlainText("reg1", blacklist="{}:?/")
Traceback (most recent call last):
NotImplementedError: ...
>>> parser = PlainText.parser(stop_symbols="/")
>>> next(parser)
>>> try:
...    for s in "man/woman":
...        parser.send(s)
... except StopIteration as result:
...    man_from_binary = result.value
>>> print(man_from_binary)
man
>>> print(repr(man_from_binary))
<PlainText: 'man', blacklist='/'>
>>> parser = PlainText.parser(stop_symbols="{")
>>> next(parser)
>>> try:
...    for s in "man{":
...        parser.send(s)
... except StopIteration as result:
...    man_from_interpolation = result.value
>>> print(man_from_interpolation)
man
>>> print(repr(man_from_interpolation))
<PlainText: 'man', blacklist='{'>
>>> man_from_binary == man_from_interpolation
True
>>> hash(man_from_binary) == hash(man_from_interpolation)
True
"""
from typing import Optional

from wa_typechecker import typechecked
from .Identifier import Identifier


class PlainText(str):
    """A plain text. See details in module description."""
    def __new__(cls, val, blacklist):
        raise NotImplementedError("use parser generator")

    @typechecked
    def __init__(self, blacklist: str):
        self.__blacklist = blacklist

    @property
    @typechecked
    def blacklist(self) -> str:
        return self.__blacklist

    def __repr__(self):
        return "<{}: {}, blacklist={}>".format(self.__class__.__name__,
                                               repr(str(self)),
                                               repr(self.__blacklist))

    @classmethod
    @typechecked
    def parser(cls, prefix: Optional[Identifier] = None, stop_symbols=""):
        """Generator

        Accepts one symbol in a row to be sent.
        Ends when a return statement raises StopIteration.
        The StopIteration value is always a PlainText.
        """
        # initialize
        string = list(str(prefix)) if prefix else []

        def result(cls):
            plain_text = super().__new__(cls, "".join(string))
            plain_text.__init__(blacklist=stop_symbols)
            return plain_text

        # get first symbol
        symbol = yield
        while symbol is not None:
            # check on success characters
            if symbol in stop_symbols:
                return result(cls)
            string.append(symbol)
            symbol = yield
        # summarize on send None
        return result(cls)
