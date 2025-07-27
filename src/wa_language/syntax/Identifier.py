"""
Tests:
# >>> Identifier("reg1")
# Traceback (most recent call last):
# NotImplementedError: ...
>>> parser = Identifier.parser()
>>> next(parser)
>>> try:
...    for s in "reg1":
...        parser.send(s)
...    next(parser)
... except StopIteration as result:
...    print(result.value)
...    print(repr(result.value))
reg1
<Identifier: 'reg1'>
>>> parser = Identifier.parser()
>>> next(parser)
>>> try:
...    for s in "fizz and buzz":
...        parser.send(s)
... except StopIteration as result:
...    print(result.value)
...    print(repr(result.value))
fizz
<Identifier: 'fizz'>
>>> parser = Identifier.parser()
>>> next(parser)
>>> try:
...    for s in "__0_s2}":
...        parser.send(s)
... except StopIteration as result:
...    print(result.value)
...    print(repr(result.value))
__0_s2
<Identifier: '__0_s2'>
>>> parser = Identifier.parser()
>>> next(parser)
>>> try:
...    for s in "s?":
...        parser.send(s)
... except StopIteration as result:
...    print(result.value)
...    print(repr(result.value))
s
<Identifier: 's'>
"""

from wa_typechecker import typechecked


class Identifier(str):
    """An identifier. See details in module description."""
    # TODO: make private constructor
    # def __new__(cls, val):
    #     raise NotImplementedError("use parser generator")

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, repr(str(self)))

    @classmethod
    @typechecked
    def parser(cls):
        """Generator

        Accepts one symbol in a row to be sent.
        Ends when a return statement raises StopIteration.
        The StopIteration value is either Identifier
        or an empty str
        """
        # initialize
        string = []
        lower_case_range = range(ord('a'), ord('z') + 1)
        upper_case_range = range(ord('A'), ord('Z') + 1)
        underscore_ord = ord('_')
        digit_range = None  # will be created after first symbol check

        def result(cls):
            if string:
                # create Identifier
                return super().__new__(cls, "".join(string))
            else:
                # return empty str because empty str could not be a valid Identifier
                return ""

        # get first symbol
        symbol = yield
        while symbol is not None:
            # process symbol
            ordinal = ord(symbol)
            if (
                ordinal in lower_case_range or
                ordinal in upper_case_range or
                ordinal == underscore_ord or
                (digit_range is not None and ordinal in digit_range)
            ):
                string.append(symbol)
            else:
                return result(cls)
            # create digit range if needed
            if digit_range is None:
                digit_range = range(ord('0'), ord('9')+1)
            # get next symbol
            symbol = yield
        # summarize on send None
        return result(cls)
