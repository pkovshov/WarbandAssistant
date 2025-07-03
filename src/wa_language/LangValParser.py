"""Parse string resources

Each string resource is an Interpolation (Interpolation object).
It could be
- Empty string
- Plain string that does not contain fields
- Interpolation with the fields
Example of Interpolation with the fields:
'As you wish, {sire/my lady}. {reg6?I:{reg7?You:{s11}}} will be the new {reg3?lady:lord} of {s1}.'

An Interpolation splits into a sequence of items
where each item may be
- a plain string (str object)
- a field (Field object)

So, empty and plain strings are represented by Interpolations with one string item only.

In string resources there could be three types on field expressions:
- An Identifier (Identifier object).
  Examples of Fields with Identifier:
  - '{s9}'
  - '{reg5}'
- Binary expressions (Binary object)
  It is two plain or empty strings separated by slash '/'.
  Examples of Fields with a Binary expression:
  - '{lord/lady}'
  - '{sir/madam}'
- Ternary expression (Ternary object)
  It's an identifier followed by a question mark '?' and two interpolations separated by a colon ':'.
  Each interpolation may be an empty string a plain string or may contain several fields.
  This leads to nested expressions.
  Examples of Fields with a Ternary expression:
  - {reg7?them:him}
  - {reg6?I:{reg7?You:{s11}}}
  - {reg3?Me and {reg4?{reg3} of my mates:one of my mates} are:I am}
"""

import re
from typing import List, Tuple, Union

from typeguard import typechecked


class Expression:
    def __repr__(self):
        return f"{self.__class__.__name__}({repr(str(self))})"


class Field:
    """A field in the interpolation. See details in module description.
    """
    def __init__(self, src: str):
        self.__expr = parse_field(src)

    @property
    def expression(self):
        return self.__expr

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.__expr == other.__expr
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__expr)

    def __str__(self):
        return "{" + str(self.expression) + "}"

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(str(self))})"


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
    ValueError: ...
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
        obj.__raw = raw
        return obj

    @property
    def items(self) -> Tuple[Union[str, Field], ...]:
        return self.__items

    @property
    def fields(self) -> Tuple[Field, ...]:
        return self.__fields

    @property
    def raw(self) -> bool:
        return self.__raw

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(str(self))})"


class Identifier(Expression):
    """
    An identifier expression. See details in module description.

    Tests:
    >>> ident_1 = Identifier('s3')
    >>> print(ident_1.value)
    s3
    >>> print(ident_1)
    s3
    >>> print(repr(ident_1))
    Identifier('s3')
    >>> ident_1 == eval(repr(ident_1))
    True
    >>> ident_2 = Identifier('reg5')
    >>> ident_1 == ident_2
    False
    >>> hash(ident_1) == hash(ident_2)
    False
    >>> ident_3 = Identifier('s3')
    >>> ident_1 == ident_3
    True
    >>> hash(ident_1) == hash(ident_3)
    True
    >>> Identifier("2")
    Traceback (most recent call last):
    ValueError: ...
    """
    @typechecked
    def __init__(self, src: str):
        self.__item = parse_identifier(src)

    @property
    def value(self) -> str:
        return self.__item

    def __eq__(self, other):
        if isinstance(other, Identifier):
            return self.__item == other.__item
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__item)

    def __str__(self):
        return self.__item


class Binary(Expression):
    """
    A Binary expression. See details in module description.

    Tests:
    >>> binar_1 = Binary('lord/lady')
    >>> print(binar_1.first)
    lord
    >>> print(binar_1.second)
    lady
    >>> print(binar_1)
    lord/lady
    >>> print(repr(binar_1))
    Binary('lord/lady')
    >>> binar_1 == eval(repr(binar_1))
    True
    >>> binar_2 = Binary('sir/madam')
    >>> binar_1 == binar_2
    False
    >>> hash(binar_1) == hash(binar_2)
    False
    >>> binar_3 = Binary('lord/lady')
    >>> binar_1 == binar_3
    True
    >>> hash(binar_1) == hash(binar_3)
    True
    >>> Binary("sir/madam/her")
    Traceback (most recent call last):
    ValueError: ...
    """
    @typechecked
    def __init__(self, src: str):
        self.__items = parse_binary(src)

    @property
    def first(self) -> str:
        return self.__items[0]

    @property
    def second(self) -> str:
        return self.__items[1]

    def __eq__(self, other):
        if isinstance(other, Binary):
            return self.__items == other.__items
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__items)

    def __iter__(self):
        return iter(self.__items)

    def __str__(self):
        return f"{self.first}/{self.second}"


class Ternary(Expression):
    @typechecked
    def __init__(self, src: str):
        self.__items = parse_ternary(src)

    @property
    def condition(self) -> Identifier:
        return self.__items[0]

    @property
    def true_part(self) -> Interpolation:
        return self.__items[1]

    @property
    def false_part(self) -> Interpolation:
        return self.__items[2]

    def __eq__(self, other):
        if isinstance(other, Ternary):
            return self.__items == other.__items
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__items)

    def __iter__(self):
        return iter(self.__items)

    def __str__(self):
        return f"{self.condition}?{self.true_part}:{self.false_part}"


@typechecked
def parse_identifier(src: str) -> str:
    """Parse an expression as an identifier.
    Tests:
    >>> parse_identifier("s6")
    's6'
    >>> parse_identifier("reg14")
    'reg14'
    >>> parse_identifier("Ac97_342")
    'Ac97_342'
    >>> parse_identifier("__76wqe")
    '__76wqe'
    >>> parse_identifier("x")
    'x'
    >>> parse_identifier("_")
    '_'
    >>> parse_identifier("G")
    'G'
    >>> parse_identifier("5")
    Traceback (most recent call last):
    ValueError: ...
    >>> parse_identifier("86")
    Traceback (most recent call last):
    ValueError: ...
    >>> parse_identifier("s6:")
    Traceback (most recent call last):
    ValueError: ...
    >>> parse_identifier("s6?")
    Traceback (most recent call last):
    ValueError: ...
    """
    if re.fullmatch("([a-z]|[A-Z]|_)([a-z]|[A-Z]|_|[0-9])*", src):
        return src
    else:
        raise ValueError("Not an identifier: " + repr(src))


@typechecked
def parse_binary(src: str) -> Tuple[str, str]:
    """Parse an expression as a binary.

    Tests:
    >>> parse_binary("lord/lady")
    ('lord', 'lady')
    >>> parse_binary("q4 qIK _+?/")
    ('q4 qIK _+?', '')
    >>> parse_binary("/")
    ('', '')
    >>> parse_binary("Greeting.")
    Traceback (most recent call last):
    ValueError: ...
    >>> parse_binary("he/she/her")
    Traceback (most recent call last):
    ValueError: ...
    >>> parse_binary("{reg1}/ok")
    Traceback (most recent call last):
    ValueError: ...
    """
    if src.find("{") > 0 or src.find("}") > 0:
        raise ValueError("Not a binary: " + repr(src))
    if src.find("/") < 0:
        raise ValueError("Not a binary: " + repr(src))
    split = src.split("/")
    if len(split) != 2:
        raise ValueError("Not a binary: " + repr(src))
    return split[0], split[1]


@typechecked
def parse_ternary(src: str) -> Tuple[Identifier, Interpolation, Interpolation]:
    """Parse an expression as a ternary.

    # Tests:
    >>> parse_ternary('reg7?them:him')
    (Identifier('reg7'), Interpolation('them'), Interpolation('him'))
    """
    if src.find("?") < 0:
        raise ValueError("Not an ternary: " + repr(src))
    split = src.split("?", maxsplit=1)
    if len(split) != 2:
        raise ValueError("Not an ternary: " + repr(src))
    condition, tail = split
    tail = split[1]
    depth = 0
    for pos, char in enumerate(tail):
        if char == ":":
            if depth == 0:
                break
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        if depth < 0:
            raise ValueError("Not an ternary: " + repr(src))
    else:
        raise ValueError("Not an ternary: " + repr(src))
    true_expr = tail[:pos]
    false_expr = tail[pos+1:]
    try:
        return Identifier(condition), Interpolation(true_expr), Interpolation(false_expr)
    except ValueError:
        raise ValueError("Not an ternary: " + repr(src))


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
        raise ValueError("Not an interpolation: " + repr(src))
    if prev_pos != len(src):
        items.append(src[prev_pos:])
    return items


@typechecked
def parse_field(src: str) -> Expression:
    """Parse a field and return a corresponding expression

    Tests:
    >>> parse_field("{reg14}")
    Identifier('reg14')
    >>> parse_field("{lad/lass}")
    Binary('lad/lass')
    """
    if src[0] != "{" or src[-1] != "}":
        raise ValueError("Not a field: " + repr(src))
    expr = src[1:-1]
    try:
        return Identifier(expr)
    except ValueError:
        pass
    try:
        return Binary(expr)
    except ValueError:
        pass
    try:
        return Ternary(expr)
    except ValueError:
        pass
    raise ValueError("Not a field: " + repr(src))


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)


