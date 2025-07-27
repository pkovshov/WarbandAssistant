"""
Tests:
>>> parser_ = parser()
>>> next(parser_)
>>> try:
...     for s in "{reg1}":
...         parser_.send(s)
... except StopIteration as stop:
...     result = stop.value
>>> isinstance(result, IdentifierExpression)
True
>>> print(result)
{reg1}
>>> print(result.identifier)
reg1
>>> parser_ = parser()
>>> next(parser_)
>>> try:
...     for s in "{man/woman}":
...         parser_.send(s)
... except StopIteration as stop:
...     result = stop.value
>>> isinstance(result, BinaryExpression)
True
>>> print(result)
{man/woman}
>>> print(result.left, result.right)
man woman
"""

from .Identifier import Identifier
from .PlainText import PlainText
from .IdentifierExpression import IdentifierExpression
from .BinaryExpression import BinaryExpression
from .TernaryExpression import TernaryExpression
from .Interpolation import Interpolation


def parser():
    """Generator

    Accepts one symbol in a row to be sent.
    Ends when a return statement raises StopIteration.
    The StopIteration value is either Expression
    or a str instance if expression syntax was violated.
    """
    first_symbol = "{"
    items = []
    symbol = yield
    if symbol != "{":
        # expression must start with {
        return ""
    identifier_parser = Identifier.parser()
    next(identifier_parser)
    symbol = yield
    try:
        while symbol is not None:
            identifier_parser.send(symbol)
            symbol = yield
        next(identifier_parser)
    except StopIteration as stop:
        identifier = stop.value
    if symbol == "}":
        if identifier == "":
            return first_symbol
        else:
            return IdentifierExpression(identifier)
    elif symbol == "?":
        if identifier == "":
            return first_symbol
        else:
            items.append(identifier)
        true_part_parser = Interpolation.parser(stop_symbol=":")
        next(true_part_parser)
        symbol = yield
        try:
            while symbol is not None:
                true_part_parser.send(symbol)
                symbol = yield
            next(true_part_parser)
        except StopIteration as stop:
            true_part = stop.value
            assert isinstance(true_part, list)
            true_part = Interpolation(true_part)
        items.append(true_part)
        if symbol is None:
            # TODO: log warning
            return first_symbol + "".join(str(item) for item in items)
        false_part_parser = Interpolation.parser(stop_symbol="}")
        next(false_part_parser)
        symbol = yield
        try:
            while symbol is not None:
                false_part_parser.send(symbol)
                symbol = yield
            next(false_part_parser)
        except StopIteration as stop:
            false_part = stop.value
            assert isinstance(false_part, list)
            false_part = Interpolation(false_part)
        items.append(false_part)
        if symbol != "}":
            # TODO: log warning
            return first_symbol + str(items[0]) + "?" + str(items[1]) + ":" + str(items[2])
        if (
            len(items) == 3 and
            isinstance(items[0], Identifier) and
            isinstance(items[1], Interpolation) and
            isinstance(items[2], Interpolation)
        ):
            return TernaryExpression(tuple(items))
        else:
            # TODO: log warning
            return first_symbol + "".join(str(item) for item in items)
    else:
        binary_parser = (BinaryExpression.parser([first_symbol])
                         if identifier == "" else
                         BinaryExpression.parser([first_symbol, identifier]))
        next(binary_parser)
        try:
            while symbol is not None:
                binary_parser.send(symbol)
                symbol = yield
            next(binary_parser)
        except StopIteration as stop:
            binary = stop.value
        return binary

