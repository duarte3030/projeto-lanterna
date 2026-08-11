HearthomeCityGymTrainerRoom2_MapScripts::
	.byte 0

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

HearthomeCityGymTrainerRoom2_EventScript_SchoolKidMackenzie::
	trainerbattle_single TRAINER_SINNOH_SCHOOL_KID_MACKENZIE, HearthomeCityGymTrainerRoom2_Text_SchoolKidMackenzieIntro, HearthomeCityGymTrainerRoom2_Text_SchoolKidMackenzieDefeat
	msgbox HearthomeCityGymTrainerRoom2_Text_SchoolKidMackenziePost, MSGBOX_AUTOCLOSE
	end

HearthomeCityGymTrainerRoom2_Text_SchoolKidMackenzieIntro:
	.string "Eek! That's so bright!\pSurprise attack!$"

HearthomeCityGymTrainerRoom2_Text_SchoolKidMackenzieDefeat:
	.string "Your strength is dazzling!\nI have to shield my eyes!$"

HearthomeCityGymTrainerRoom2_Text_SchoolKidMackenziePost:
	.string "I'm going over the reasons why I\nlost. That way, I'll win next time.$"

HearthomeCityGymTrainerRoom2_EventScript_AceTrainerAllen::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_ALLEN, HearthomeCityGymTrainerRoom2_Text_AceTrainerAllenIntro, HearthomeCityGymTrainerRoom2_Text_AceTrainerAllenDefeat
	msgbox HearthomeCityGymTrainerRoom2_Text_AceTrainerAllenPost, MSGBOX_AUTOCLOSE
	end

HearthomeCityGymTrainerRoom2_Text_AceTrainerAllenIntro:
	.string "What, were you just dawdling around\nhoping I'd notice you for a battle?\pYou know you're going to get whupped\nhere, don't you?$"

HearthomeCityGymTrainerRoom2_Text_AceTrainerAllenDefeat:
	.string "I kinda deserved that, didn't I?\nI gotta stop mouthing off like that...$"

HearthomeCityGymTrainerRoom2_Text_AceTrainerAllenPost:
	.string "I'll remember you and your shifty\nPokémon, too. I'm watching you...$"

HearthomeCityGymTrainerRoom2_EventScript_SchoolKidChance::
	trainerbattle_single TRAINER_SINNOH_SCHOOL_KID_CHANCE, HearthomeCityGymTrainerRoom2_Text_SchoolKidChanceIntro, HearthomeCityGymTrainerRoom2_Text_SchoolKidChanceDefeat
	msgbox HearthomeCityGymTrainerRoom2_Text_SchoolKidChancePost, MSGBOX_AUTOCLOSE
	end

HearthomeCityGymTrainerRoom2_Text_SchoolKidChanceIntro:
	.string "Are you lost?\nAre you enjoying yourself?$"

HearthomeCityGymTrainerRoom2_Text_SchoolKidChanceDefeat:
	.string "Let me guess.\nYou are enjoying yourself.$"

HearthomeCityGymTrainerRoom2_Text_SchoolKidChancePost:
	.string "Whatever happens in life, it's better to\ntry to enjoy it the best one can.\pBeing in the dark here, I came to\nrealize that.$"

HearthomeCityGymTrainerRoom2_EventScript_AceTrainerCatherine::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_CATHERINE, HearthomeCityGymTrainerRoom2_Text_AceTrainerCatherineIntro, HearthomeCityGymTrainerRoom2_Text_AceTrainerCatherineDefeat
	msgbox HearthomeCityGymTrainerRoom2_Text_AceTrainerCatherinePost, MSGBOX_AUTOCLOSE
	end

HearthomeCityGymTrainerRoom2_Text_AceTrainerCatherineIntro:
	.string "What does it feel like, taking one step\nafter another into darkness?$"

HearthomeCityGymTrainerRoom2_Text_AceTrainerCatherineDefeat:
	.string "You're the kind of person who can keep\ngoing forward even into the unknown.$"

HearthomeCityGymTrainerRoom2_Text_AceTrainerCatherinePost:
	.string "I think, sometimes, one has to make\nmistakes to learn what is right.$"
