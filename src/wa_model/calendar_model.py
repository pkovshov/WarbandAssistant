from wa_typechecker import typechecked
from wa_language.LangVar import LangVar
from wa_language.KeyChecker import key_checker
from wa_language.Spreading import Spreading, Spread, EMPTY_SPREADING


is_timeofday_key = key_checker("ui_midnight",
                               "ui_late_night",
                               "ui_dawn",
                               "ui_early_morning",
                               "ui_morning",
                               "ui_noon",
                               "ui_afternoon",
                               "ui_late_afternoon",
                               "ui_dusk",
                               "ui_evening")

timeofday_model = {is_timeofday_key: EMPTY_SPREADING}

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

is_date_key = key_checker(__date_key_to_month)

YEAR_VAR = LangVar("reg2")
DAY_VAR = LangVar("reg1")

date_model = {
    is_date_key: Spreading({YEAR_VAR: Spread(range(1257, 1278)),
                            DAY_VAR: Spread(range(1, 32))})
}


@typechecked
def month(date_key: str):
    return __date_key_to_month[date_key]
