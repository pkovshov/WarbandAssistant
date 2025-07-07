from enum import Enum

from typeguard import typechecked


__date_key_to_month = {
    "str_january_reg1_reg2": 1,
    "str_february_reg1_reg2": 2,
    "str_march_reg1_reg2": 3,
    "str_april_reg1_reg2": 4,
    "str_may_reg1_reg2": 5,
    "str_june_reg1_reg2": 6,
    "str_july_reg1_reg2": 7,
    "str_august_reg1_reg2": 8,
    "str_september_reg1_reg2": 9,
    "str_october_reg1_reg2": 10,
    "str_november_reg1_reg2": 11,
    "str_december_reg1_reg2": 12
}


@typechecked
def is_date_key(key: str) -> bool:
    return key in __date_key_to_month


@typechecked
def month(date_key: str):
    return __date_key_to_month[date_key]


class DateVariables(Enum):
    Year = "reg2"
    Day = "reg1"


MIN_YEAR = 1257


@typechecked
def is_timeofday_key(key: str) -> bool:
    return key in ("ui_midnight",
                   "ui_late_night",
                   "ui_dawn",
                   "ui_early_morning",
                   "ui_morning",
                   "ui_noon",
                   "ui_afternoon",
                   "ui_late_afternoon",
                   "ui_dusk",
                   "ui_evening")

