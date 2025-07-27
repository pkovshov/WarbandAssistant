from abc import ABC, abstractmethod
from typing import Any, Tuple

from wa_typechecker import typechecked


class Expression(ABC):
    def __init__(self, items: Tuple[Any, ...]):
        self.__items = items

    @property
    def _items(self) -> Tuple[Any, ...]:
        return self.__items

    def __eq__(self, other):
        if isinstance(other, Expression):
            return self.__items == other.__items
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__items)

    @abstractmethod
    def __str__(self):
        raise NotImplemented

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ", ".join(repr(item) for item in self.__items))

    # @staticmethod
    # def parser():
    #     """Generator
    #
    #     Accepts one symbol in a row to be sent.
    #     Ends when a return statement raises StopIteration.
    #     The StopIteration value is either Expression
    #     or a str instance if expression syntax was violated.
    #     """
    #     items = []
    #     symbol = yield
    #     if symbol != "{":
    #         # expression must start with {
    #         return ""
    #     identifier_parser = Identifier.parser(stop_symbols="?}")
    #     next(identifier_parser)
    #     try:
    #         symbol = yield
    #         while symbol is not None:
    #             identifier_parser.send(symbol)
    #             symbol = yield
    #         next(identifier_parser)
    #     except StopIteration as result:
    #         identifier_result = result.value
    #     if isinstance(identifier_result, Identifier):
    #         items.append(identifier_result)
    #         if symbol == "}":
    #             return IdentifierExpression(items)
    #         else:
    #             # TODO: use Interpolation parser
    #             pass
    #     else:
    #         # TODO: use Binary parser
    #         pass




