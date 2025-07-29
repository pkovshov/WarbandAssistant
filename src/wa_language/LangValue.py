from functools import partial
from typing import Any, FrozenSet, Iterable, List, Set, Union, TYPE_CHECKING
import logging

from wa_typechecker import typechecked
from .syntax.Errors import LangSyntaxError
from .syntax.Expression import Expression
from .syntax.IdentifierExpression import IdentifierExpression
from .syntax.BinaryExpression import BinaryExpression
from .syntax.TernaryExpression import TernaryExpression
from .syntax.Interpolation import Interpolation
from .LangKey import LangKey
from .LangVar import LangVar, PlayerSexVar
from .Binding import Binding, EMPTY_BINDING, PlayerSex
from .Spreading import SpreadType
if TYPE_CHECKING:
    from .Language import Language


class LangValue(str):
    @typechecked
    def __new__(cls, source: Union[str, Interpolation], lang: "Language", key: LangKey):
        if isinstance(source, Interpolation):
            inst = super().__new__(cls, str(source))
            inst._interpolation = source
        else:
            inst = super().__new__(cls, source)
            try:
                inst._interpolation = Interpolation(source)
            except LangSyntaxError as error:
                logging.getLogger(__name__).warning(
                    f"Syntax error. Use raw mode with value: '{key}|{source}' Error: {error}")
                inst._interpolation = Interpolation(source, raw=True)
        inst.__lang = lang
        inst.__key = key
        inst.__variables = None
        inst.__conditions = None
        return inst

    @property
    def key(self) -> LangKey:
        return self.__key

    @property
    def lang(self) -> "Language":
        return self.__lang

    @property
    def variables(self) -> FrozenSet[LangVar]:
        if self.__variables is None:
            self.__build_variables_and_conditions()
        return self.__variables

    @property
    def conditions(self) -> FrozenSet[LangVar]:
        if self.__conditions is None:
            self.__build_variables_and_conditions()
        return self.__conditions

    @property
    def binding(self) -> Binding:
        return EMPTY_BINDING

    @typechecked
    def bind(self, variable: LangVar, value: Any) -> "LangValue":
        if variable not in self.variables:
            return self
        bound_interpolation = bind_interpolation(self._interpolation,
                                                 variable=variable,
                                                 value=value)
        binding = Binding({variable: value})
        return LangValueBound(interpolation=bound_interpolation,
                              binding=binding,
                              origin=self)

    @typechecked
    def spread(self, variable: LangVar, value_spread: SpreadType) -> list["LangValue"]:
        spread = []
        for value in value_spread:
            spread.append(self.bind(variable, value))
        return spread

    def __build_variables_and_conditions(self):
        variables = set()
        conditions = set()
        build_variables_and_conditions(self._interpolation, variables, conditions)
        self.__variables = frozenset(variables)
        self.__conditions = frozenset(conditions)


class LangValueBound(LangValue):
    @typechecked
    def __new__(cls, interpolation: Interpolation, binding: Binding, origin: LangValue):
        inst = super().__new__(cls, interpolation, origin.lang, origin.key)
        inst.__binding = binding
        inst.__origin = origin
        return inst

    @property
    def binding(self) -> Binding:
        return self.__binding

    @typechecked
    def bind(self, variable: LangVar, value: Any) -> "LangValue":
        if variable in self.__binding:
            if self.__binding[variable] == value:
                return self
            else:
                raise ValueError(f"try to re-bing {variable} variable "
                                 f"from {self.__binding[variable]} "
                                 f"to {value}")
        else:
            if variable not in self.__origin.variables:
                return self
            if variable not in self.variables:
                bound_interpolation = self._interpolation
            else:
                bound_interpolation = bind_interpolation(self._interpolation,
                                                         variable=variable,
                                                         value=value)
            binding = self.__binding | {variable: value}
            return LangValueBound(interpolation=bound_interpolation,
                                  binding=binding,
                                  origin=self.__origin)


@typechecked
def build_variables_and_conditions(interpolation: Interpolation,
                                   variables: Set[LangVar],
                                   conditions: Set[LangVar]):
    for item in interpolation.items:
        if isinstance(item, IdentifierExpression):
            variables.add(LangVar(item.identifier))
        elif isinstance(item, BinaryExpression):
            variables.add(PlayerSexVar)
        elif isinstance(item, TernaryExpression):
            variables.add(LangVar(item.condition))
            conditions.add(LangVar(item.condition))
            build_variables_and_conditions(item.true_part, variables, conditions)
            build_variables_and_conditions(item.false_part, variables, conditions)


@typechecked
def _bind_interpolation_item(item: Union[str, Expression],
                             variable: LangVar,
                             value: Any) -> Union[str, Expression, Interpolation]:
    if isinstance(item, IdentifierExpression) and item.identifier == variable:
        return str(value)
    elif isinstance(item, BinaryExpression) and variable == PlayerSexVar:
        if value is PlayerSex.MALE:
            return item.left
        elif value is PlayerSex.FEMALE:
            return item.right
        else:
            raise ValueError(f"PlayerSex variable must be bound with PlayerSex value, got {value}")
    elif isinstance(item, TernaryExpression):
        if variable == item.condition:
            if value:
                return bind_interpolation(item.true_part, variable, value, compress = False)
            else:
                return bind_interpolation(item.false_part, variable, value, compress = False)
        else:
            return TernaryExpression(item.condition,
                                     bind_interpolation(item.true_part, variable, value),
                                     bind_interpolation(item.false_part, variable, value))
    else:
        return item


@typechecked
def _compress_interpolation_items(input_items: Iterable[Union[str, Expression, Interpolation]],
                                  output_items: List[Union[str, Expression]],
                                  string_buffer: List[str]):
    for item in input_items:
        if isinstance(item, str):
            string_buffer.append(item)
        elif isinstance(item, Expression):
            if string_buffer:
                output_items.append("".join(string_buffer))
                string_buffer.clear()
            output_items.append(item)
        elif isinstance(item, Interpolation):
            _compress_interpolation_items(item.items, output_items, string_buffer)
        else:
            assert False


@typechecked
def bind_interpolation(interpolation: Interpolation,
                       variable: LangVar,
                       value: Any,
                       compress=True) -> Interpolation:
    bind_items_iter = map(partial(_bind_interpolation_item,
                                  value=value,
                                  variable=variable),
                          interpolation.items)
    if compress:
        items = []
        buffer = []
        _compress_interpolation_items(input_items=bind_items_iter,
                                      output_items=items,
                                      string_buffer=buffer)
        if buffer:
            items.append("".join(buffer))
        return Interpolation(tuple(items))
    else:
        return Interpolation(tuple(bind_items_iter))
