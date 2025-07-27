"""
Tests:
>>> interp = Interpolation("Hello")
>>> interp.items
('Hello',)
>>> interp.identifiers
()
>>> interp.conditions
()
>>> interp.raw
False
>>> list(interp)
['H', 'e', 'l', 'l', 'o']
>>> interp[1:4]
'ell'
>>> interp == "Hello"
True
>>> hash(interp) == hash("Hello")
True
>>> interp = Interpolation("{reg14}")
>>> interp.items
(IdentifierExpression('reg14'),)
>>> interp.identifiers
('reg14',)
>>> interp.conditions
()
>>> interp.raw
False
>>> interp[4]
'1'
>>> interp.upper()
'{REG14}'
>>> 'reg' in interp
True
>>> interp = Interpolation("{s")
Traceback (most recent call last):
wa_language.syntax.Errors.LangSyntaxError: ...
>>> interp = Interpolation("{s", True)
>>> interp.items
('{s',)
>>> interp.identifiers
()
>>> interp.conditions
()
>>> interp.raw
True
>>> from .TernaryExpression import TernaryExpression
>>> result = Interpolation("Hi:{sir/lady}")
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

from typing import Tuple, Union

from wa_typechecker import typechecked
from .Expression import Expression
from .IdentifierExpression import IdentifierExpression
from .BinaryExpression import BinaryExpression


class Interpolation(str):
    @typechecked
    def __new__(cls, source: Union[str, Tuple[Union[Expression, str], ...]], raw: bool = False):
        """
        :param source: Source string or collection of items (str and/or Expression)
        :param raw: Do not parse source string. Default = false
        """
        if raw:
            if isinstance(source, str):
                items = source,
                string = source
            else:
                raise TypeError(f"for raw mode source must be a str, got {repr(source)}")
        else:
            if isinstance(source, str):
                from .parser import parse_interpolation
                items = parse_interpolation(source)
                string = source
            else:
                items = source
                string = "".join(str(item) for item in items)
        # TODO: move variables and conditions calculation to LangValue
        from .TernaryExpression import TernaryExpression
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
                raise TypeError(f"items must be Expression or str, got {repr(item)}")
        obj = super().__new__(cls, string)
        obj.__items: Tuple[Union[Expression, str], ...] = items
        obj.__identifiers = tuple(identifiers)
        obj.__conditions = tuple(conditions)
        obj.__has_binary = has_binary
        obj.__raw = raw
        return obj

    @property
    def raw(self):
        return self.__raw

    @property
    def has_binary(self) -> bool:
        return self.__has_binary

    @property
    def items(self) -> Tuple[Union[str, Expression], ...]:
        return self.__items

    @property
    def identifiers(self) -> Tuple[str, ...]:
        return self.__identifiers

    @property
    def conditions(self) -> Tuple[str, ...]:
        return self.__conditions

    # TODO: move substitute to LangValue
    @typechecked
    def substitute(self, variable: str, value: str) -> "Interpolation":
        """Substitute all the identifiers with same name by the given variable
        >>> interp = Interpolation("{s1}, {s2} yes {s1?{s2}:{reg3}}")
        >>> print(interp.substitute("s1", "Joe Dou"))
        Joe Dou, {s2} yes {s2}
        >>> print(interp.substitute("s1", ""))
        , {s2} yes {reg3}
        >>> print(interp.substitute("s2", "Ricki"))
        {s1}, Ricki yes {s1?Ricki:{reg3}}
        """
        from .TernaryExpression import TernaryExpression
        from wa_language.Language import (BINARY_CONDITION_VARIABLE,
                                          BINARY_CONDITION_VARIABLE_FIRST_VALUE,
                                          BINARY_CONDITION_VARIABLE_SECOND_VALUE)

        def substitute_item(item: Union[Expression, str]) -> Union[Expression, str]:
            from .TernaryExpression import TernaryExpression
            if isinstance(item, IdentifierExpression) and item.identifier == variable:
                return value
            elif isinstance(item, BinaryExpression) and variable == BINARY_CONDITION_VARIABLE:
                if value == BINARY_CONDITION_VARIABLE_FIRST_VALUE:
                    return item.left
                elif value == BINARY_CONDITION_VARIABLE_SECOND_VALUE:
                    return item.right
            elif isinstance(item, TernaryExpression):
                if variable == item.condition:
                    if value == "":
                        return item.false_part.substitute(variable, value)
                    else:
                        return item.true_part.substitute(variable, value)
                else:
                    return TernaryExpression(item.condition, item.true_part.substitute(variable, value),
                                             item.false_part.substitute(variable, value))
            else:
                return item

        items = []
        buffer = []
        for item in map(substitute_item, self.__items):
            if isinstance(item, str):
                buffer.append(item)
            else:
                if buffer:
                    items.append("".join(buffer))
                    buffer.clear()
                items.append(item)
        if buffer:
            items.append("".join(buffer))
        return Interpolation(tuple(items))

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
        return "{}({}{})".format(self.__class__.__name__,
                                 ", ".join(repr(item) for item in self.__items),
                                 ", raw = True" if self.__raw else "")
