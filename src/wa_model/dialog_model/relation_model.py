from wa_language.LangVar import LangVar
from wa_language.KeyChecker import key_checker
from wa_language.Spreading import Spreading, Spread

is_relation_key = key_checker("str_relation_reg1",
                              "str_morale_reg1")

RELATION_VAR = LangVar("reg1")

relation_model_seed = {
    is_relation_key: Spreading({RELATION_VAR: Spread(range(-100, 101))})
}
