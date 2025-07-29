"""
Tests:
>>> from .BinaryExpression import BinaryExpression
>>> from .TernaryExpression import TernaryExpression
>>> interp = Interpolation("Hello")
>>> interp.items
('Hello',)
>>> interp.raw
False
>>> interp = Interpolation("{reg14}")
>>> interp.items
(IdentifierExpression('reg14'),)
>>> interp.raw
False
>>> interp = Interpolation("{s")
Traceback (most recent call last):
wa_language.syntax.Errors.LangSyntaxError: ...
>>> interp = Interpolation("{s", True)
>>> interp.items
('{s',)
>>> interp.raw
True
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


class Interpolation:
    @typechecked
    def __init__(self, source: Union[str, Tuple[Union[Expression, str], ...]], raw: bool = False):
        """
        :param source: Source string or collection of items (str and/or Expression)
        :param raw: Do not parse source string. Default = false
        """
        if not raw:
            if isinstance(source, str):
                items = parse_interpolation(source)
            else:
                items = source
        else:
            if isinstance(source, str):
                items = source,
            else:
                raise TypeError(f"for the raw mode a source param must be an instance of str, got {repr(source)}")
        self.__items = items
        self.__raw = raw

    @property
    def raw(self) -> bool:
        return self.__raw

    @property
    def items(self) -> Tuple[Union[str, Expression], ...]:
        return self.__items

    def __str__(self):
        return "".join(str(item) for item in self.__items)

    def __repr__(self):
        return "{}({}{})".format(self.__class__.__name__,
                                 ", ".join(repr(item) for item in self.__items),
                                 ", raw = True" if self.__raw else "")


from .parser import parse_interpolation
