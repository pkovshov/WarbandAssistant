from functools import partial
from typing import overload, Any, FrozenSet, Iterable, Iterator, List, Mapping, NamedTuple, Set, Union, TYPE_CHECKING
import logging

from wa_typechecker import typechecked
from .syntax.Errors import LangSyntaxError
from .syntax.Expression import Expression
from .syntax.IdentifierExpression import IdentifierExpression
from .syntax.BinaryExpression import BinaryExpression
from .syntax.TernaryExpression import TernaryExpression
from .syntax.Interpolation import Interpolation
from .LangKey import LangKey
from .LangVar import LangVar, PlayerSexVar, PlayerSex, EMPTY_STR, FALSE_EMPTY_STR, TRUE_EMPTY_STR
from .Spreading import Spreading, Spread
from .Binding import Binding, EMPTY_BINDING

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

    @overload
    def bind(self, variable: LangVar, value: Any) -> "LangValue":
        ...

    @overload
    def bind(self, binding: Binding) -> "LangValue":
        ...

    def bind(self, *args, **kwargs) -> "LangValue":
        if kwargs:
            raise TypeError("Keyword arguments are not supported")
        if len(args) == 2:
            return self._bind_with_pair(*args)
        elif len(args) == 1:
            return self._bind_with_binding(args[0])
        else:
            raise TypeError(f"bind got insufficient args: {', '.join(repr(arg) for arg in args)}")

    @overload
    def spread(self, variable: LangVar, value_spread: Spread) -> Iterator["LangValue"]:
        ...

    @overload
    def spread(self, spreading: Spreading) -> Iterator["LangValue"]:
        ...

    def spread(self, *args, **kwargs) -> Iterator["LangValue"]:
        if kwargs:
            raise TypeError("Keyword arguments are not supported")
        if len(args) == 2:
            return self.__spread_with_pair(*args)
        elif len(args) == 1:
            return self.__spread_with_spreading(args[0])
        else:
            raise TypeError(f"spread got insufficient args: {', '.join(repr(arg) for arg in args)}")

    def purge_spread(self) -> Iterator["LangValue"]:
        conditions_only = self.conditions
        variables_only = self.variables - self.conditions
        if PlayerSexVar not in variables_only:
            # TODO: prevent copying within Binding and Spreading __init__
            binding = Binding({var: EMPTY_STR for var in variables_only})
            spreading = Spreading({var: Spread(TRUE_EMPTY_STR, FALSE_EMPTY_STR)
                                 for var in conditions_only})
        else:
            # TODO: prevent copying within Binding and Spreading __init__
            binding = Binding({var: EMPTY_STR for var in variables_only
                               if var is not PlayerSexVar})
            spreading = {var: Spread(TRUE_EMPTY_STR, FALSE_EMPTY_STR)
                         for var in conditions_only}
            spreading[PlayerSexVar] = Spread(PlayerSex.MALE, PlayerSex.FEMALE)
            spreading = Spreading(spreading)
        return self.bind(binding).spread(spreading)

    @typechecked
    def _bind_with_pair(self, variable: LangVar, value: Any) -> "LangValue":
        if variable not in self.variables:
            return self
        bound_interpolation = bind_interpolation_with_pair(self._interpolation,
                                                           variable=variable,
                                                           value=value)
        binding = Binding({variable: value})
        return LangValueBound(interpolation=bound_interpolation,
                              binding=binding,
                              origin=self)

    @typechecked
    def _bind_with_binding(self, binding: Binding) -> "LangValue":
        if len(binding) == 0:
            return self
        binding = dict(binding)
        for var in list(binding):
            if var not in self.variables:
                del binding[var]
        if len(binding) == 0:
            return self
        binding = Binding(binding)
        bound_interpolation = bind_interpolation_with_mapping(self._interpolation,
                                                              binding=binding)
        return LangValueBound(interpolation=bound_interpolation,
                              binding=binding,
                              origin=self)

    @typechecked
    def __spread_with_pair(self,
                           variable: LangVar,
                           variable_values: Spread) -> Iterator["LangValue"]:
        if variable in self.variables:
            return (self.bind(variable, value) for value in variable_values)
        else:
            return iter([self])

    @typechecked
    def __spread_with_spreading(self, spreading: Spreading) -> Iterator["LangValue"]:
        result_spread = iter([self])
        for var, spread in spreading.items():
            def gen(lang_values, variable, variable_values):
                for lang_value in lang_values:
                    yield from lang_value.__spread_with_pair(variable, variable_values)
            result_spread = gen(result_spread, var, spread)
        return result_spread

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
    def _bind_with_pair(self, variable: LangVar, value: Any) -> "LangValue":
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
                bound_interpolation = bind_interpolation_with_pair(self._interpolation,
                                                                   variable=variable,
                                                                   value=value)
            binding = self.__binding | {variable: value}
            return LangValueBound(interpolation=bound_interpolation,
                                  binding=binding,
                                  origin=self.__origin)

    @typechecked
    def _bind_with_binding(self, binding: Binding) -> "LangValue":
        if len(binding) == 0:
            return self
        binding = dict(binding)
        for var, value in list(binding.items()):
            if var in self.__binding:
                if self.__binding[var] == value:
                    del binding[var]
                else:
                    raise ValueError(f"try to re-bing {var} variable "
                                     f"from {self.__binding[var]} "
                                     f"to {value}")
            elif var not in self.__origin.variables:
                del binding[var]
        binding_to_perform = {var: val for var, val in binding.items()
                              if var in self.variables}
        if len(binding_to_perform) == 0:
            bound_interpolation = self._interpolation
        else:
            bound_interpolation = bind_interpolation_with_mapping(self._interpolation,
                                                                  binding=binding_to_perform)
        binding = self.__binding | binding
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
def _bind_interpolation_item_with_pair(item: Union[str, Expression],
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
                return bind_interpolation_with_pair(item.true_part, variable, value, compress=False)
            else:
                return bind_interpolation_with_pair(item.false_part, variable, value, compress=False)
        else:
            return TernaryExpression(item.condition,
                                     bind_interpolation_with_pair(item.true_part, variable, value),
                                     bind_interpolation_with_pair(item.false_part, variable, value))
    else:
        return item


@typechecked
def bind_interpolation_with_pair(interpolation: Interpolation,
                                 variable: LangVar,
                                 value: Any,
                                 compress=True) -> Interpolation:
    bind_items_iter = map(partial(_bind_interpolation_item_with_pair,
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


@typechecked
def _bind_interpolation_item_with_mapping(item: Union[str, Expression],
                                          binding: Mapping[str, Any]) -> Union[str, Expression, Interpolation]:
    if isinstance(item, IdentifierExpression) and item.identifier in binding:
        return str(binding[item.identifier])
    elif isinstance(item, BinaryExpression) and PlayerSexVar in binding:
        player_sex = binding[PlayerSexVar]
        if player_sex is PlayerSex.MALE:
            return item.left
        elif player_sex is PlayerSex.FEMALE:
            return item.right
        else:
            raise ValueError(f"PlayerSex variable must be bound with PlayerSex value, got {repr(player_sex)}")
    elif isinstance(item, TernaryExpression):
        if item.condition in binding:
            if binding[item.condition]:
                return bind_interpolation_with_mapping(item.true_part, binding, compress=False)
            else:
                return bind_interpolation_with_mapping(item.false_part, binding, compress=False)
        else:
            return TernaryExpression(item.condition,
                                     bind_interpolation_with_mapping(item.true_part, binding),
                                     bind_interpolation_with_mapping(item.false_part, binding))
    else:
        return item


@typechecked
def bind_interpolation_with_mapping(interpolation: Interpolation,
                                    binding: Mapping[str, Any],
                                    compress=True) -> Interpolation:
    bind_items_iter = map(partial(_bind_interpolation_item_with_mapping,
                                  binding=binding),
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
