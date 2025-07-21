from ..LangKeyChecker import key_checker
from wa_language.model.types import LordPersonality

# TODO: for philosophy use "dlga_lord_recruit_2_philosophy:lord_recruit_2" key with bind s43 to
#       "str_political_philosophy_martial",
#       "str_political_philosophy_quarrelsome"
#       "str_political_philosophy_pitiless"
#       "str_political_philosophy_cunning"
#       "str_political_philosophy_sadistic"
#       "str_political_philosophy_goodnatured"
#       "str_political_philosophy_upstanding"

is_martial_private_chat_body_key = key_checker(
    # bad relation < -5
    "str_please_do_not_take_this_amiss_but_i_do_not_trust_you",
    # insufficient -5 <= relation < 19
    "str_forgive_me_but_im_not_one_for_going_off_in_corners_to_plot",
    # enough 19 <= relation
    "str_im_a_simple__man_not_one_for_intrigue_but_id_guess_that_you_have_something_worthwhile_to_say_what_is_it",
)

is_badtempered_private_chat_body_key = key_checker(
    # bad relation
    "str_bah_i_dont_like_you_that_much_im_not_going_to_go_plot_with_you_in_some_corner",
    # insufficient relation
    "str_bah__im_in_no_mood_for_whispering_in_the_corner",
    # enough relation
    "str_all_right_then_what_do_you_have_to_say_out_with_it",
)

is_pitiless_private_chat_body_key = key_checker(
    # bad relation - same with sadistic !
    # "str_hah_i_trust_you_as_a_i_would_a_serpent_i_think_not",
    # insufficient relation
    "str_what_do_you_take_me_for_a_plotter",
    # enough relation
    "str_thats_sensible__the_world_is_full_of_churls_who_poke_their_noses_into_their_betters_business_now_tell_me_what_it_is_that_you_have_to_say"
)

is_cunning_private_chat_body_key = key_checker(
    # insufficient relation
    "str_em_lets_keep_our_affairs_out_in_the_open_for_the_time_being",
    # enough relation
    "str_hmm_you_have_piqued_my_interest_what_do_you_have_to_say",
)

is_sadistic_private_chat_body_key = key_checker(
    # bad relation - same with pitiless !
    # "str_hah_i_trust_you_as_a_i_would_a_serpent_i_think_not",
    # insufficient relation
    "str_trying_our_hand_at_intrigue_are_we_i_think_not",
    # enough relation
    "str_well__now_what_do_you_have_to_propose"
)

is_goodnatured_private_chat_body_key = key_checker(
    # insufficient relation
    "str_surely_we_can_discuss_whatever_you_want_to_discuss_out_here_in_the_open_cant_we",
    # enough relation
    "str_well_i_normally_like_to_keep_things_out_in_the_open_but_im_sure_someone_like_you_would_not_want_to_talk_in_private_unless_heshe_had_a_good_reason_what_is_it"
)

is_upstanding_private_chat_body_key = key_checker(
    # bad relation
    "str_do_not_take_this_amiss_but_with_you_i_would_prefer_to_conduct_our_affairs_out_in_the_open",
    # insufficient relation
    "str_i_would_prefer_to_conduct_our_affairs_out_in_the_open",
    # enough relation
    "str_i_do_not_like_to_conduct_my_business_in_the_shadows_but_sometimes_it_must_be_done_what_do_you_have_to_say",
)

private_chat_keys_by_lord_personality = {
    LordPersonality.MARTIAL: is_martial_private_chat_body_key,
    LordPersonality.BADTEMPERED: is_badtempered_private_chat_body_key,
    LordPersonality.PITILESS: is_pitiless_private_chat_body_key,
    LordPersonality.CUNNING: is_cunning_private_chat_body_key,
    LordPersonality.SADISTIC: is_sadistic_private_chat_body_key,
    LordPersonality.GOODNATURED: is_goodnatured_private_chat_body_key,
    LordPersonality.UPSTANDING: is_upstanding_private_chat_body_key
}

is_private_chat_key = key_checker(private_chat_keys_by_lord_personality.values())
