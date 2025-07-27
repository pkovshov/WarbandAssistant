"""
Tests:
>>> from .TernaryExpression import TernaryExpression
>>> result = Interpolation("Hi:{sir/lady}")
>>> isinstance(result, Interpolation)
True
>>> print(result)
Hi:{sir/lady}
>>> len(result.items)
2
>>> isinstance(result.items[0], str)
True
>>> print(result.items[0])
Hi:
>>> isinstance(result.items[1], BinaryExpression)
True
>>> print(result.items[1].left, result.items[1].right)
sir lady
>>> result = Interpolation("{sister/brother}, Greetings!")
>>> isinstance(result, Interpolation)
True
>>> print(result)
{sister/brother}, Greetings!
>>> len(result.items)
2
>>> isinstance(result.items[0], BinaryExpression)
True
>>> print(result.items[0].left, result.items[0].right)
sister brother
>>> isinstance(result.items[1], str)
True
>>> print(result.items[1])
, Greetings!
>>> result = Interpolation("{reg1?{reg2}:Hello {sir/madam} from {s1?me:us}} and welcome")
>>> isinstance(result, Interpolation)
True
>>> print(result)
{reg1?{reg2}:Hello {sir/madam} from {s1?me:us}} and welcome
>>> len(result.items)
2
>>> isinstance(result.items[0], TernaryExpression)
True
>>> print(result.items[0].condition, result.items[0].true_part, result.items[0].false_part)
reg1 {reg2} Hello {sir/madam} from {s1?me:us}
>>> print(len(result.items[0].true_part.items))
1
>>> print(result.items[0].true_part.items[0].identifier)
reg2
>>> print(len(result.items[0].false_part.items))
4
>>> print(*result.items[0].false_part.items, sep='|')
Hello |{sir/madam}| from |{s1?me:us}
>>> isinstance(result.items[0].false_part.items[1], BinaryExpression)
True
>>> isinstance(result.items[0].false_part.items[3], TernaryExpression)
True
>>> isinstance(result.items[1], str)
True
>>> print(result.items[1])
 and welcome
"""

from collections.abc import Collection
from typing import Any, Iterable, Iterator, Tuple, Union

from wa_typechecker import typechecked
from .Expression import Expression
from .PlainText import PlainText
from .Identifier import Identifier
from .IdentifierExpression import IdentifierExpression
from .BinaryExpression import BinaryExpression


class Interpolation(str):
    @typechecked
    def __new__(cls, src: str | list, raw: bool = False):
        """
        :param src: Source string.
        :param raw: Do not parse source string. Default = false
        """
        from .TernaryExpression import TernaryExpression
        if isinstance(src, str):
            parser = Interpolation.parser()
            next(parser)
            try:
                for ch in src:
                    parser.send(ch)
                next(parser)
            except StopIteration as stop:
                items = tuple(stop.value)
        else:
            items = tuple(src)
        has_binary = False
        identifiers = set()
        conditions = set()
        for item in items:
            if isinstance(item, IdentifierExpression):
                identifiers.add(item.identifier)
            elif isinstance(item, BinaryExpression):
                has_binary = True
            elif isinstance(item, TernaryExpression):
                identifiers.add(item.condition)
                identifiers |= set(item.true_part.identifiers + item.false_part.identifiers)
                conditions.add(item.condition)
                conditions |= set(item.true_part.conditions + item.false_part.conditions)
            elif isinstance(item, str):
                pass
            else:
                raise TypeError(f"items must be Expression or str, but got {item}")
        obj = super().__new__(cls, "".join(str(item) for item in items))
        obj.__items = items
        obj.__identifiers = tuple(identifiers)
        obj.__conditions = tuple(conditions)
        obj.__has_binary = has_binary
        return obj

    @property
    def has_binary(self) -> bool:
        return self.__has_binary

    @property
    def items(self) -> Tuple[Identifier, ...]:
        return self.__items

    @property
    def identifiers(self) -> Tuple[Identifier, ...]:
        return self.__identifiers

    @property
    def conditions(self) -> Tuple[Identifier, ...]:
        return self.__conditions

    # # TODO: Deprecated
    # @property
    # @typechecked
    # def items(self) -> Tuple[Union[str, Expression], ...]:
    #     return self.__items

    @typechecked
    def substitute(self, variable: Identifier, value: str) -> "Interpolation":
        from .TernaryExpression import TernaryExpression
        from wa_language.Language import (BINARY_CONDITION_VARIABLE,
                                          BINARY_CONDITION_VARIABLE_FIRST_VALUE,
                                          BINARY_CONDITION_VARIABLE_SECOND_VALUE)
        """Substitute all the identifiers with same name by the given variable
        >>> interp = Interpolation("{s1}, {s2} yes {s1?{s2}:{reg3}}")
        >>> print(interp.substitute(Identifier("s1"), "Joe Dou"))
        Joe Dou, {s2} yes {s2}
        >>> print(interp.substitute(Identifier("s1"), ""))
        , {s2} yes {reg3}
        >>> print(interp.substitute(Identifier("s2"), "Ricki"))
        {s1}, Ricki yes {s1?Ricki:{reg3}}
        """
        items = list(self.__items)
        for idx, item in enumerate(items):
            if isinstance(item, IdentifierExpression) and item.identifier == variable:
                items[idx] = value
            elif isinstance(item, BinaryExpression) and variable == BINARY_CONDITION_VARIABLE:
                if value == BINARY_CONDITION_VARIABLE_FIRST_VALUE:
                    items[idx] = item.left
                elif value == BINARY_CONDITION_VARIABLE_SECOND_VALUE:
                    items[idx] = item.right
            elif isinstance(item, TernaryExpression):
                if variable == item.condition:
                    if value == "":
                        items[idx] = str(item.false_part)
                    else:
                        items[idx] = str(item.true_part)
                else:
                    items[idx] = f"{{{item.condition}?{item.true_part.substitute(variable,value)}:{item.false_part.substitute(variable,value)}}}"
            else:
                items[idx] = str(item)
        return Interpolation("".join(items))

    # @typechecked
    # def spread(self, variables_and_values: Mapping[str, Iterable[str]]) -> List["Interpolation"]:
    #     """Build a list of substitutions
    #
    #     Tests:
    #     >>> interp = Interpolation("{s1}, {s2} yes {s1?{s2}:{reg3}}")
    #     >>> spread = interp.spread({"s1": ["ko", "ro"], "s2": ["jjj", "erq"]})
    #     >>> spread.sort()
    #     >>> print(*spread, sep='\\n')
    #     ko, erq yes erq
    #     ko, jjj yes jjj
    #     ro, erq yes erq
    #     ro, jjj yes jjj
    #     >>> interp = Interpolation("{ma/fa}, {s2} yes {s1?{s2}:{reg3}}")
    #     >>> spread = interp.spread({"wa_binary": ["first"], "s2": ["jjj", "erq"]})
    #     >>> spread.sort()
    #     >>> print(*spread, sep='\\n')
    #     ma, erq yes {s1?erq:{reg3}}
    #     ma, jjj yes {s1?jjj:{reg3}}
    #     """
    #     spread_list = [self]
    #     for variable, values in variables_and_values.items():
    #         for idx, interp in enumerate(spread_list):
    #             spread_list[idx] = [interp.substitute(variable, value) for value in values]
    #         spread_list = list(itertools.chain.from_iterable(spread_list))
    #     return spread_list

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ", ".join(repr(item) for item in self.__items))

    @classmethod
    def parser(cls, stop_symbol=None):
        from . import expression_parser
        string = []
        items = []
        parser = None
        symbol = yield

        def work_with_parser():
            nonlocal parser
            try:
                parser.send(symbol)
            except StopIteration as stop:
                parser = None
                result = stop.value
                if isinstance(result, Expression):
                    items.append(result)
                else:
                    # TODO: log warning
                    return result

        while symbol is not None:
            if parser:
                violator = work_with_parser()
                if violator is not None:
                    if items and isinstance(items[-1], str):
                        string = list(items.pop() + violator)
                    else:
                        string = list(violator)
                    continue  # for processing one more time a symbol that breaks syntax
            elif symbol == "{":
                if string:
                    items.append("".join(string))
                    string = []
                parser = expression_parser.parser()
                next(parser)
                parser.send(symbol)
            elif symbol != stop_symbol:
                string.append(symbol)
            else:
                if string:
                    items.append("".join(string))
                return items
            symbol = yield

        if parser:
            violator = work_with_parser()
            if violator is not None:
                if items and isinstance(items[-1], str):
                    items[-1] = items[-1] + violator
                else:
                    items.append(violator)
        elif string:
            items.append("".join(string))

        return items
