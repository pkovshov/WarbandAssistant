import pytest

from wa_language.Language import RootLanguage
from wa_language.LangKey import LangKey
from wa_language.LangVar import LangVar, PlayerSexVar, PLAYER_NAME_VAR, PlayerSex
from wa_language.Spreading import Spread
from wa_language.Binding import Binding


def test_lang_var():
    reg_var_1 = LangVar("reg")
    assert repr(reg_var_1) == "LangVar('reg')"
    assert str(reg_var_1) == "reg"
    assert hash(reg_var_1) == hash("reg")
    assert reg_var_1 == "reg"
    assert "reg" == reg_var_1
    assert not reg_var_1 != "reg"
    assert not "reg" != reg_var_1

    reg_var_2 = LangVar("reg")
    assert reg_var_2 is not reg_var_1
    assert reg_var_2 == reg_var_1
    assert not reg_var_2 != reg_var_1
    assert hash(reg_var_2) == hash(reg_var_1)

    reg_var_3 = LangVar("s")
    assert reg_var_3 != reg_var_1
    assert not reg_var_3 == reg_var_1
    assert hash(reg_var_3) != hash(reg_var_1)

    assert repr(PlayerSexVar) == "PlayerSexVar"
    assert PlayerSexVar == PlayerSexVar
    assert not PlayerSexVar != PlayerSexVar
    sex_var = type(PlayerSexVar)()
    assert sex_var is PlayerSexVar
    assert sex_var == PlayerSexVar

    assert str(PlayerSexVar) == ""
    assert PlayerSexVar != ""
    assert "" != PlayerSexVar
    assert not PlayerSexVar == ""
    assert not "" == PlayerSexVar

    assert str(PlayerSexVar) != "wow"
    assert PlayerSexVar != "wow"
    assert "wow" != PlayerSexVar
    assert not PlayerSexVar == "wow"
    assert not "wow" == PlayerSexVar

    empty_var = LangVar("")
    assert str(empty_var) == str(PlayerSexVar)
    assert hash(empty_var) != hash(sex_var)
    assert not empty_var == PlayerSexVar
    assert not PlayerSexVar == empty_var
    assert empty_var != PlayerSexVar
    assert PlayerSexVar != empty_var

    assert str(reg_var_1) != str(PlayerSexVar)
    assert hash(reg_var_1) != hash(sex_var)
    assert reg_var_1 != PlayerSexVar
    assert PlayerSexVar != reg_var_1
    assert not reg_var_1 == PlayerSexVar
    assert not PlayerSexVar == reg_var_1

    player_name = LangVar("playername")
    assert player_name is not PLAYER_NAME_VAR
    assert str(player_name) == str(PLAYER_NAME_VAR)
    assert player_name == PLAYER_NAME_VAR
    assert PLAYER_NAME_VAR == player_name
    assert not player_name != PLAYER_NAME_VAR
    assert not PLAYER_NAME_VAR != player_name
    assert hash(player_name) == hash(PLAYER_NAME_VAR)


def test_variables_and_conditions():
    lang = RootLanguage({
        "tst_key": "As you wish, {sire/my lady}. {reg6?I:{reg7?You:{s11}}} will be the new {reg3?lady:lord} of {s1}."
    })
    lang_value = next(iter(lang.values()))
    assert isinstance(lang_value, str)
    assert lang_value.variables == {PlayerSexVar, "reg6", "reg7", "s11", "reg3", "s1"}
    assert lang_value.conditions == {"reg6", "reg7", "reg3"}


def test_bind_lang_values():
    lang = RootLanguage({
        "tst_key": "As you wish, {sire/my lady}. {reg6?I:{reg7?{Sir/Lady}, you:{s11}}} will be the new {reg3?lady:lord} of {s1}.",
    })
    lang_value = next(iter(lang.values()))
    assert len(lang_value.binding) == 0
    male_value = lang_value.bind(PlayerSexVar, PlayerSex.MALE)
    assert "As you wish, sire. {reg6?I:{reg7?Sir, you:{s11}}} will be the new {reg3?lady:lord} of {s1}." == male_value
    assert {PlayerSexVar: PlayerSex.MALE} == male_value.binding
    female_value = lang_value.bind(PlayerSexVar, PlayerSex.FEMALE)
    assert "As you wish, my lady. {reg6?I:{reg7?Lady, you:{s11}}} will be the new {reg3?lady:lord} of {s1}." == female_value
    assert {PlayerSexVar: PlayerSex.FEMALE} == female_value.binding
    bound_value = lang_value.bind(LangVar("reg6"), True)
    assert "As you wish, {sire/my lady}. I will be the new {reg3?lady:lord} of {s1}." == bound_value
    assert {LangVar("reg6"): True} == bound_value.binding
    bound_value = lang_value.bind(LangVar("s11"), "wow!")
    assert "As you wish, {sire/my lady}. {reg6?I:{reg7?{Sir/Lady}, you:wow!}} will be the new {reg3?lady:lord} of {s1}." == bound_value
    assert {LangVar("s11"): "wow!"} == bound_value.binding

    lang = RootLanguage({
        "tst_control": "We control {reg13?{reg13} towns:}"
    })
    control_value = lang["tst_control"]
    bound_value = control_value.bind(LangVar("reg13"), 0)
    assert "We control " == bound_value
    assert {LangVar("reg13"): 0} == bound_value.binding
    bound_value = control_value.bind(LangVar("reg13"), 5)
    assert "We control 5 towns" == bound_value
    assert {LangVar("reg13"): 5} == bound_value.binding
    assert control_value == control_value.bind(PlayerSexVar, PlayerSex.MALE)
    assert len(control_value.bind(PlayerSexVar, PlayerSex.MALE).binding) == 0
    assert control_value == control_value.bind(LangVar("s6"), "warriors")
    assert len(control_value.bind(LangVar("s6"), "warriors").binding) == 0


def test_bind_bound_lang_values():
    lang = RootLanguage({
        "tst_key": "As you wish, {sire/my lady}. {reg6?I:{reg7?{Sir/Lady}, you:{s11}}} will be the new {reg3?lady:lord} of {s1}.",
    })
    lang_value = next(iter(lang.values()))
    male_value = lang_value.bind(PlayerSexVar, PlayerSex.MALE)
    with pytest.raises(ValueError):
        male_value.bind(PlayerSexVar, PlayerSex.FEMALE)
    male_value = male_value.bind(PlayerSexVar, PlayerSex.MALE)
    male_value = male_value.bind(LangVar("reg6"), False)
    male_value = male_value.bind(LangVar("reg7"), True)
    with pytest.raises(ValueError):
        male_value.bind(LangVar("reg6"), True)
    assert "As you wish, sire. Sir, you will be the new {reg3?lady:lord} of {s1}." == male_value
    assert {PlayerSexVar: PlayerSex.MALE, "reg6": False, "reg7": True} == male_value.binding
    # variable s11 is added to binding due to it was in origin value
    # but as far as it's absent in current bound - it does not affect the value
    same_male_value = male_value.bind(LangVar("s11"), "welcome")
    assert same_male_value == male_value
    assert same_male_value.binding != male_value.binding
    assert {PlayerSexVar: PlayerSex.MALE, "reg6": False, "reg7": True, "s11": "welcome"} == same_male_value.binding
    # variable nonono is not added to binding
    same_male_value = male_value.bind(LangVar("nonono"), "ha-ha")
    assert same_male_value == male_value
    # s11 was added to binding due to it was in origin value
    assert same_male_value.binding == male_value.binding


def test_bind_with_dict_lang_values():
    lang = RootLanguage({
        "tst_key": "As you wish, {sire/my lady}. {reg6?I:{reg7?{Sir/Lady}, you:{s11}}} will be the new {reg3?lady:lord} of {s1}.",
    })
    lang_value = next(iter(lang.values()))
    male_value = lang_value.bind(Binding({PlayerSexVar: PlayerSex.MALE, LangVar("reg7"): True}))
    assert "As you wish, sire. {reg6?I:Sir, you} will be the new {reg3?lady:lord} of {s1}." == male_value
    assert {PlayerSexVar: PlayerSex.MALE, LangVar("reg7"): True} == male_value.binding
    female_value = lang_value.bind(Binding({PlayerSexVar: PlayerSex.FEMALE, LangVar("reg7"): False}))
    assert "As you wish, my lady. {reg6?I:{s11}} will be the new {reg3?lady:lord} of {s1}." == female_value
    assert {PlayerSexVar: PlayerSex.FEMALE, LangVar("reg7"): False} == female_value.binding
    bound_value = lang_value.bind(Binding({LangVar("reg6"): False, LangVar("s11"): "Santa Claus", PlayerSexVar: PlayerSex.MALE}))
    assert "As you wish, sire. {reg7?Sir, you:Santa Claus} will be the new {reg3?lady:lord} of {s1}." == bound_value
    assert {LangVar("reg6"): False, LangVar("s11"): "Santa Claus", PlayerSexVar: PlayerSex.MALE} == bound_value.binding
    bound_value = lang_value.bind(Binding({LangVar("s11"): "wow!", LangVar("s1"): 15}))
    assert "As you wish, {sire/my lady}. {reg6?I:{reg7?{Sir/Lady}, you:wow!}} will be the new {reg3?lady:lord} of 15." == bound_value
    assert {LangVar("s11"): "wow!", LangVar("s1"): 15} == bound_value.binding

    lang = RootLanguage({
        "tst_control": "We control {reg13?{reg13} towns:}"
    })
    control_value = lang["tst_control"]
    bound_value = control_value.bind(Binding({LangVar("reg13"): 0, PlayerSexVar: PlayerSex.MALE}))
    assert "We control " == bound_value
    assert {LangVar("reg13"): 0} == bound_value.binding

# TODO: test bind with binding for bound lang values
# def test_bind_with_dict_bound_lang_values():
#     lang = RootLanguage({
#         "tst_key": "As you wish, {sire/my lady}. {reg6?I:{reg7?{Sir/Lady}, you:{s11}}} will be the new {reg3?lady:lord} of {s1}.",
#     })
#     lang_value = next(iter(lang.values()))
#     male_value = lang_value.bind(PlayerSexVar, PlayerSex.MALE)
#     with pytest.raises(ValueError):
#         male_value.bind(PlayerSexVar, PlayerSex.FEMALE)
#     male_value = male_value.bind(PlayerSexVar, PlayerSex.MALE)
#     male_value = male_value.bind(LangVar("reg6"), False)
#     male_value = male_value.bind(LangVar("reg7"), True)
#     with pytest.raises(ValueError):
#         male_value.bind(LangVar("reg6"), True)
#     assert "As you wish, sire. Sir, you will be the new {reg3?lady:lord} of {s1}." == male_value
#     assert {PlayerSexVar: PlayerSex.MALE, "reg6": False, "reg7": True} == male_value.binding
#     # variable s11 is added to binding due to it was in origin value
#     # but as far as it's absent in current bound - it does not affect the value
#     same_male_value = male_value.bind(LangVar("s11"), "welcome")
#     assert same_male_value == male_value
#     assert same_male_value.binding != male_value.binding
#     assert {PlayerSexVar: PlayerSex.MALE, "reg6": False, "reg7": True, "s11": "welcome"} == same_male_value.binding
#     # variable nonono is not added to binding
#     same_male_value = male_value.bind(LangVar("nonono"), "ha-ha")
#     assert same_male_value == male_value
#     # s11 was added to binding due to it was in origin value
#     assert same_male_value.binding == male_value.binding


def test_binding():
    dct_1: dict = {LangVar('a'): 1,
                   LangVar('b'): 2,
                   LangVar('c'): 3}
    dct_2: dict = {LangVar('a'): 4}
    binding_1 = Binding(dct_1)
    binding_2 = Binding(dct_2)
    assert binding_1 | binding_2 == dct_1 | dct_2
    assert binding_2 | binding_1 == dct_2 | dct_1
    assert binding_1 | dct_2 == dct_1 | dct_2
    assert dct_2 | binding_1 == dct_2 | dct_1


def test_spread():
    def check_with_collection(collect):
        spread = Spread(collect)
        assert len(spread) == len(collect)
        assert list(spread) == list(collect)
        assert bool(spread) == bool(collect)
        assert (not spread) == (not collect)
        for item in spread:
            assert item in collect
        for item in collect:
            assert item in spread

    def check_with_empty_collection(value):
        with pytest.raises(ValueError):
            Spread(value)

    def check_with_wrong_type(value):
        with pytest.raises(TypeError):
            Spread(value)

    check_with_collection(range(1, 10))
    check_with_collection(range(12))
    check_with_collection(range(-5, 20, 3))
    check_with_collection((1, -5, 19, 0.8, True, False, None, 'A', 'qW-er', 19, [1, 2, 'qer'], {1, 4, 9}))
    check_with_collection(tuple(range(12)))

    check_with_empty_collection(range(0))
    check_with_empty_collection(tuple())


    check_with_wrong_type("Hello")
    check_with_wrong_type([1, 2, 3])
    check_with_wrong_type({'a', 'b', 'c', 'd'})
    check_with_wrong_type(iter(range(5)))
    check_with_wrong_type(i**2 for i in range(4))

    # TODO: add test for Spread.__init__ with several args or with empty args

def test_purge_spread_with_unbind_sex_var():
    lang = RootLanguage({
        "tst_key": "As you wish, {sire/my lady}. {reg6?I:Wee} glad to see {s11}",
    })
    lang_value = next(iter(lang.values()))
    purge_spread = sorted(lang_value.purge_spread())
    assert purge_spread == [
        "As you wish, my lady. I glad to see ",
        "As you wish, my lady. Wee glad to see ",
        "As you wish, sire. I glad to see ",
        "As you wish, sire. Wee glad to see ",
    ]

def test():
    lang = RootLanguage({
        "tst_greet": "Greetings, {sir/lady} {playername}"
    })
    assert lang["tst_greet"] == "Greetings, {sir/lady} {playername}"
    key_1 = LangKey("s6")
    key_2 = LangKey(key_1)
