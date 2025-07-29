import re
from typing import Tuple, Union

from wa_typechecker import typechecked
from .Errors import LangSyntaxError
from .Expression import Expression
from .IdentifierExpression import IdentifierExpression
from .BinaryExpression import BinaryExpression
from .TernaryExpression import TernaryExpression
from .Interpolation import Interpolation


@typechecked
def parse_field(src: str) -> Expression:
    """Parse a field and return a corresponding expression

    Tests:
    >>> parse_field("{reg14}")
    IdentifierExpression('reg14')
    >>> parse_field("{lad/lass}")
    BinaryExpression('lad', 'lass')
    >>> parse_field("reg14")
    Traceback (most recent call last):
    wa_language.syntax.Errors.LangSyntaxError: ...
    >>> parse_field("{x?x?x}")
    Traceback (most recent call last):
    wa_language.syntax.Errors.LangSyntaxError: ...
    """
    if src[0] != "{" or src[-1] != "}":
        raise LangSyntaxError("Not a field: " + repr(src))
    expr = src[1:-1]
    return parse_expression(expr)


@typechecked
def parse_expression(expr: str) -> Expression:
    try:
        return parse_identifier(expr)
    except LangSyntaxError:
        pass
    try:
        return parse_binary(expr)
    except LangSyntaxError:
        pass
    try:
        return parse_ternary(expr)
    except LangSyntaxError:
        pass
    raise LangSyntaxError("Not an expression: " + repr(expr))


@typechecked
def parse_identifier(src: str) -> IdentifierExpression:
    """Parse an expression as an identifier.
    Tests:
    >>> parse_identifier("s6")
    IdentifierExpression('s6')
    >>> parse_identifier("reg14")
    IdentifierExpression('reg14')
    >>> parse_identifier("Ac97_342")
    IdentifierExpression('Ac97_342')
    >>> parse_identifier("__76wqe")
    IdentifierExpression('__76wqe')
    >>> parse_identifier("x")
    IdentifierExpression('x')
    >>> parse_identifier("_")
    IdentifierExpression('_')
    >>> parse_identifier("G")
    IdentifierExpression('G')
    >>> parse_identifier("5")
    Traceback (most recent call last):
    wa_language.syntax.Errors.LangSyntaxError: ...
    >>> parse_identifier("86")
    Traceback (most recent call last):
    wa_language.syntax.Errors.LangSyntaxError: ...
    >>> parse_identifier("s6:")
    Traceback (most recent call last):
    wa_language.syntax.Errors.LangSyntaxError: ...
    >>> parse_identifier("s6?")
    Traceback (most recent call last):
    wa_language.syntax.Errors.LangSyntaxError: ...
    """
    if re.fullmatch("([a-z]|[A-Z]|_)([a-z]|[A-Z]|_|[0-9])*", src):
        return IdentifierExpression(src)
    else:
        raise LangSyntaxError("Not an identifier: " + repr(src))


@typechecked
def parse_binary(src: str) -> BinaryExpression:
    """Parse an expression as a binary.

    Tests:
    >>> parse_binary("lord/lady")
    BinaryExpression('lord', 'lady')
    >>> parse_binary("q4 qIK _+?/")
    BinaryExpression('q4 qIK _+?', '')
    >>> parse_binary("/")
    BinaryExpression('', '')
    >>> parse_binary("Greeting.")
    Traceback (most recent call last):
    wa_language.syntax.Errors.LangSyntaxError: ...
    >>> parse_binary("he/she/her")
    Traceback (most recent call last):
    wa_language.syntax.Errors.LangSyntaxError: ...
    >>> parse_binary("{reg1}/ok")
    Traceback (most recent call last):
    wa_language.syntax.Errors.LangSyntaxError: ...
    >>> parse_binary("sir/madam/her")
    Traceback (most recent call last):
    wa_language.syntax.Errors.LangSyntaxError: ...
    """
    if src.find("{") > 0 or src.find("}") > 0:
        raise LangSyntaxError("Not a binary: " + repr(src))
    if src.find("/") < 0:
        raise LangSyntaxError("Not a binary: " + repr(src))
    split = src.split("/")
    if len(split) != 2:
        raise LangSyntaxError("Not a binary: " + repr(src))
    return BinaryExpression(split[0], split[1])


@typechecked
def parse_ternary(src: str) -> TernaryExpression:
    """Parse an expression as a ternary.

    Tests:
    >>> parse_ternary('reg7?them:him')
    TernaryExpression('reg7', Interpolation('them'), Interpolation('him'))
    """
    if src.find("?") < 0:
        raise LangSyntaxError("Not a ternary: " + repr(src))
    split = src.split("?", maxsplit=1)
    if len(split) != 2:
        raise LangSyntaxError("Not a ternary: " + repr(src))
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
            raise LangSyntaxError("Not an ternary: " + repr(src))
    else:
        raise LangSyntaxError("Not an ternary: " + repr(src))
    true_expr = tail[:pos]
    false_expr = tail[pos+1:]
    try:
        return TernaryExpression(condition,
                                 Interpolation(true_expr),
                                 Interpolation(false_expr))
    except LangSyntaxError:
        raise LangSyntaxError("Not a ternary: " + repr(src))


@typechecked
def parse_interpolation(src: str) -> Tuple[Union[str, Expression], ...]:
    """Parse string as an interpolation

    Tests:
    >>> parse_interpolation("")
    ()
    >>> parse_interpolation("aloha")
    ('aloha',)
    >>> parse_interpolation("{_80}")
    (IdentifierExpression('_80'),)
    >>> parse_interpolation("sand {fizz/buzz}")
    ('sand ', BinaryExpression('fizz', 'buzz'))
    >>> parse_interpolation("{ro?ko:} bo")
    (TernaryExpression('ro', Interpolation('ko'), Interpolation()), ' bo')
    >>> parse_interpolation("{s4}{reg8}")
    (IdentifierExpression('s4'), IdentifierExpression('reg8'))
    >>> parse_interpolation("{s4} {reg8}")
    (IdentifierExpression('s4'), ' ', IdentifierExpression('reg8'))
    >>> parse_interpolation("{s4} {reg8}")
    (IdentifierExpression('s4'), ' ', IdentifierExpression('reg8'))
    >>> items = parse_interpolation("As you wish, {sire/my lady}. {reg6?I:{reg7?You:{s11}}} will be the new {reg3?lady:lord} of {s1}.")
    >>> print(*(repr(item) for item in items), sep='\\n')
    'As you wish, '
    BinaryExpression('sire', 'my lady')
    '. '
    TernaryExpression('reg6', Interpolation('I'), Interpolation(TernaryExpression('reg7', Interpolation('You'), Interpolation(IdentifierExpression('s11')))))
    ' will be the new '
    TernaryExpression('reg3', Interpolation('lady'), Interpolation('lord'))
    ' of '
    IdentifierExpression('s1')
    '.'
    >>> items = parse_interpolation("{reg3?Me and {reg4?{reg3} of my mates:one of my mates} are:I am}")
    >>> print(len(items))
    1
    >>> items[0].condition
    'reg3'
    >>> print(*(repr(item) for item in items[0].true_part.items), sep='\\n')
    'Me and '
    TernaryExpression('reg4', Interpolation(IdentifierExpression('reg3'), ' of my mates'), Interpolation('one of my mates'))
    ' are'
    >>> items[0].false_part
    Interpolation('I am')
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
                items.append(parse_field(src[prev_pos:curr_pos+1]))
                prev_pos = curr_pos + 1
    if depth != 0:
        raise LangSyntaxError("Not an interpolation: " + repr(src))
    if prev_pos != len(src):
        items.append(src[prev_pos:])
    return tuple(items)
