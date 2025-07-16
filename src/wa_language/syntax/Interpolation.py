from typing import FrozenSet, List, Tuple, Union

from typeguard import typechecked

from .Errors import LangSyntaxError
from .Field import Field
from .Expression import Expression
from .Identifier import Identifier


class Interpolation(str):
    """An Interpolation. See details in module description.

    Tests:
    >>> interp = Interpolation("Hello")
    >>> interp.items
    ('Hello',)
    >>> interp.fields
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
    (Field('{reg14}'),)
    >>> interp.fields
    (Field('{reg14}'),)
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
    >>> interp.fields
    ()
    >>> interp.raw
    True
    """
    @typechecked
    def __new__(cls, src: str, raw: bool = False):
        """
        :param src: Source string.
        :param raw: Do not parse source string. Default = false
        """
        items = (src,) if raw else tuple(parse_interpolation(src))
        obj = super().__new__(cls, "".join(str(item) for item in items))
        obj.__items = items
        obj.__fields = tuple(item for item in items if isinstance(item, Field))
        obj.__variables = None
        obj.__raw = raw
        return obj

    @property
    @typechecked
    def items(self) -> Tuple[Union[str, Field], ...]:
        return self.__items

    @property
    @typechecked
    def fields(self) -> Tuple[Field, ...]:
        return self.__fields

    @property
    @typechecked
    def variables(self) -> FrozenSet[Identifier]:
        """Extract all the identifiers from expression tree

        Tests:
        >>> interp = Interpolation("{s1}, {s2} yes {s1?{s2}:{reg3}}")
        >>> print(*sorted(str(ident) for ident in interp.variables))
        reg3 s1 s2
        >>> interp = Interpolation("{shk}, {boy/girl}")
        >>> print(*sorted(str(ident) for ident in interp.variables))
        shk wa_binary
        """
        if self.__variables is None:
            self.__variables = frozenset()
            for field in self.fields:
                self.__variables |= field.expression.variables
        return self.__variables

    @typechecked
    def substitute(self, variable: Identifier, value: str) -> "Interpolation":
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
            if isinstance(item, Field):
                substitution = item.expression.substitute(variable, value)
                if isinstance(substitution, Expression):
                    items[idx] = str(Field(substitution))
                else:
                    items[idx] = str(substitution)
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

    @property
    @typechecked
    def raw(self) -> bool:
        return self.__raw

    def __repr__(self):
        return "{}({}{})".format(self.__class__.__name__,
                                 repr(str(self)),
                                 ", raw = True" if self.__raw else "")


@typechecked
def parse_interpolation(src: str) -> List[Union[str, Field]]:
    """Parse string as an interpolation

    Tests:
    >>> parse_interpolation("")
    []
    >>> parse_interpolation("aloha")
    ['aloha']
    >>> parse_interpolation("{_80}")
    [Field('{_80}')]
    >>> parse_interpolation("sand {fizz/buzz}")
    ['sand ', Field('{fizz/buzz}')]
    >>> parse_interpolation("{ro?ko:} bo")
    [Field('{ro?ko:}'), ' bo']
    >>> parse_interpolation("{s4}{reg8}")
    [Field('{s4}'), Field('{reg8}')]
    >>> parse_interpolation("{s4} {reg8}")
    [Field('{s4}'), ' ', Field('{reg8}')]
    >>> parse_interpolation("{s4} {reg8}")
    [Field('{s4}'), ' ', Field('{reg8}')]
    >>> parse_interpolation("As you wish, {sire/my lady}. {reg6?I:{reg7?You:{s11}}} will be the new {reg3?lady:lord} of {s1}.")
    ['As you wish, ', Field('{sire/my lady}'), '. ', Field('{reg6?I:{reg7?You:{s11}}}'), ' will be the new ', Field('{reg3?lady:lord}'), ' of ', Field('{s1}'), '.']
    >>> items = parse_interpolation("{reg3?Me and {reg4?{reg3} of my mates:one of my mates} are:I am}")
    >>> items
    [Field('{reg3?Me and {reg4?{reg3} of my mates:one of my mates} are:I am}')]
    >>> items[0].expression
    Ternary('reg3?Me and {reg4?{reg3} of my mates:one of my mates} are:I am')
    >>> items[0].expression.condition
    Identifier('reg3')
    >>> items[0].expression.false_part
    Interpolation('I am')
    >>> items[0].expression.true_part
    Interpolation('Me and {reg4?{reg3} of my mates:one of my mates} are')
    >>> items[0].expression.true_part.items
    ('Me and ', Field('{reg4?{reg3} of my mates:one of my mates}'), ' are')
    >>> items[0].expression.true_part.fields
    (Field('{reg4?{reg3} of my mates:one of my mates}'),)
    >>> items[0].expression.true_part.fields[0].expression
    Ternary('reg4?{reg3} of my mates:one of my mates')
    >>> cond, true, false = items[0].expression.true_part.fields[0].expression
    >>> cond
    Identifier('reg4')
    >>> true
    Interpolation('{reg3} of my mates')
    >>> print(*true.items, sep="|")
    {reg3}| of my mates
    >>> print(false)
    one of my mates
    """
    items = []
    depth = 0
    prev_pos = 0
    for curr_pos, char in enumerate(src):
        if char == "{":
            if depth == 0:
                if prev_pos != curr_pos:
                    items.append(src[prev_pos:curr_pos])
                    prev_pos = curr_pos
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                items.append(Field(src[prev_pos:curr_pos+1]))
                prev_pos = curr_pos + 1
    if depth != 0:
        raise LangSyntaxError("Not an interpolation: " + repr(src))
    if prev_pos != len(src):
        items.append(src[prev_pos:])
    return items


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)


