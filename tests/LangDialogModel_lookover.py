# from wa_language.Language import load, LangKey
# from wa_language.LangVar import PlayerSex
# from wa_model.dialog_model.DialogBodyModel import DialogBodyModel
#
# lang = load()
#
# for player_sex in (None, PlayerSex.MALE, PlayerSex.FEMALE):
#     print("="*80)
#     print("=", "player_sex:", None if player_sex is None else player_sex.name)
#     print("=" * 80)
#     dialog_model = DialogBodyModel(lang=lang, player_sex=player_sex)
#     yaroglek_key = LangKey("trp_kingdom_2_lord")
#     print(lang[yaroglek_key])
#     body_keys = dialog_model.get_body_keys(yaroglek_key)
#     for key in body_keys:
#         print(f"{key}|{dialog_model.get_value(key)}")
#     print(len(body_keys))
#     print()
#     clais_key = LangKey("trp_knight_1_4_pl")
#     print(lang[clais_key])
#     body_keys = dialog_model.get_body_keys(clais_key)
#     for key in body_keys:
#         print(f"{key}|{dialog_model.get_value(key)}")
#     print(len(body_keys))
#     print()
